import csv
import os
from collections import defaultdict
from urllib.parse import unquote, urlparse

import cv2
import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import file_exists, get_file_name
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(desc=f"Downloading '{file_name_with_ext}' to buffer...", total=fsize) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    """
    convert info:
    orgignal data includes DICOM(160gb)
    for convert we use prepossessed dataset that you can find here:
    https://www.kaggle.com/datasets/mohamedbenticha/cbis-ddsm ("DATA" dir)
    for tags information please download csv description:
    https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22516629#22516629accaef0469834754b89af9e007760b10
    also download dicom_info.csv from:
    https://www.kaggle.com/datasets/awsaf49/cbis-ddsm-breast-cancer-image-dataset?resource=download
    put all csv in "csv" folder
    """
    dataset_path = "DATA"
    batch_size = 50

    project_dict = defaultdict()

    csv_folder = "csv"
    info_train_calc = "calc_case_description_train_set.csv"
    info_train_mass = "mass_case_description_train_set.csv"
    info_test_calc = "calc_case_description_test_set.csv"
    info_test_mass = "mass_case_description_test_set.csv"
    ds_infos = {
        "train_calc": info_train_calc,
        "train_mass": info_train_mass,
        "test_calc": info_test_calc,
        "test_mass": info_test_mass,
    }

    project_dict = {
        "test_calc": defaultdict(),
        "test_mass": defaultdict(),
        "train_calc": defaultdict(),
        "train_mass": defaultdict(),
    }

    for ds in ds_infos:
        file = ds_infos[ds]
        temp_dict = defaultdict()
        file_path = os.path.join(csv_folder, file)
        with open(file_path, newline="") as csvfile:
            info = csv.reader(csvfile, delimiter=",")
            for i, line in enumerate(info):
                if i == 0:
                    dict_values = line
                else:
                    temp_dict[line[0] + line[2]] = {dict_values[i]: el for i, el in enumerate(line)}
            project_dict[ds] = temp_dict

    dicom_info = os.path.join(csv_folder, "dicom_info.csv")
    dicom_dict = defaultdict()

    with open(dicom_info, newline="") as csvfile:
        info = csv.reader(csvfile, delimiter=",")
        for i, line in enumerate(info):
            if i == 0:
                dict_values = line
            else:
                dicom_dict[line[17]] = {dict_values[i]: el for i, el in enumerate(line)}

    tag_dict = defaultdict()
    image_test = []
    image_train = []

    for r, d, f in os.walk(dataset_path):
        for file in f:
            if "MASK" not in file:
                file_key = file[: file.find("_FULL")]
                try:
                    for key in dicom_dict:
                        if file_key in key:
                            tag_dict[file] = dicom_dict[key]
                            if "Test" in r:
                                image_test.append(os.path.join(r, file))
                            else:
                                image_train.append(os.path.join(r, file))
                            break
                except Exception:
                    pass

    def get_corr_key(dict, key1, key2):
        try:
            info = dict[key1]
        except Exception:
            info = dict[key2]
        return info

    def get_mask_path(path, name):
        dir_path, filename = os.path.split(path)
        for file in os.listdir(dir_path):
            if name in file and file != filename:
                return os.path.join(dir_path, file)

    def create_ann(image_path):
        labels = []
        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]
        info = tag_dict[os.path.basename(image_path)]
        pation_id = "P_" + info["PatientID"].split("_")[2] + info["PatientID"].split("_")[3]
        if "Test" in image_path and "Calc" in image_path:
            k = "test_calc"
        elif "Test" in image_path and "Mass" in image_path:
            k = "test_mass"
        elif "Train" in image_path and "Calc" in image_path:
            k = "train_calc"
        elif "Train" in image_path and "Mass" in image_path:
            k = "train_mass"
        try:
            pat_info = project_dict[k][pation_id]
        except Exception:
            pass
        img_name = os.path.basename(image_path)
        mask_path = get_mask_path(image_path, img_name[0 : img_name.find("_FULL")])
        tags_sly = []
        tags = [
            pat_info["pathology"],
            pat_info["abnormality type"],
            info["PatientOrientation"],
            info["PatientID"].split("_")[3],
            "assessment:" + pat_info["assessment"],
        ]
        if pat_info["abnormality type"] == "mass":
            tags_any = {
                "mass_margins": get_corr_key(pat_info, "mass_margins", "mass margins"),
                "mass_shape": get_corr_key(pat_info, "mass_shape", "mass shape"),
                "breast_density": get_corr_key(pat_info, "breast_density", "breast density"),
                "patient_id": get_corr_key(pat_info, "patient_id", "patient id"),
                "subtlety": pat_info["subtlety"],
            }
        else:
            tags_any = {
                "calc_type": get_corr_key(pat_info, "calc_type", "calc type"),
                "calc_distribution_list": get_corr_key(
                    pat_info, "calc_distribution_list", "calc distribution"
                ),
                "breast_density": get_corr_key(pat_info, "breast_density", "breast density"),
                "patient_id": get_corr_key(pat_info, "patient_id", "patient id"),
                "subtlety": pat_info["subtlety"],
            }

        for tag_name in tags:
            tag = [sly.Tag(tag_meta) for tag_meta in tag_metas if tag_meta.name == tag_name.lower()]
            tags_sly.append(tag[0])

        for tag_key in tags_any:
            tag = [
                sly.Tag(meta=tag_meta, value=tags_any[tag_key])
                for tag_meta in tag_metas
                if tag_meta.name == tag_key.lower()
            ]
            tags_sly.append(tag[0])

        if file_exists(mask_path):
            mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
            if len(np.unique(mask_np)) != 1:
                uniq = np.unique(mask_np)
                for label in uniq:
                    if label == 0:
                        pass
                    else:
                        obj_mask = mask_np == label
                        obj_class = meta.get_obj_class("abnormal_structure")
                        ret, curr_mask = cv2.connectedComponents(
                            mask_np.astype("uint8"), connectivity=8
                        )
                        for i in range(1, ret):
                            obj_mask = curr_mask == i
                            curr_bitmap = sly.Bitmap(obj_mask)
                            if curr_bitmap.area < 15:
                                continue
                            curr_label = sly.Label(curr_bitmap, obj_class)
                            labels.append(curr_label)
        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags_sly)

    obj_class = sly.ObjClass("abnormal_structure", sly.Bitmap, [255, 0, 0])
    tag_names_nontype = [
        "calcification",
        "RIGHT",
        "BENIGN_WITHOUT_CALLBACK",
        "MLO",
        "mass",
        "BENIGN",
        "MALIGNANT",
        "LEFT",
        "CC",
        "assessment:1",
        "assessment:2",
        "assessment:3",
        "assessment:4",
        "assessment:5",
        "assessment:0",
    ]

    tag_names_anystirng = [
        "calc_type",
        "calc_distribution",
        "mass_shape",
        "mass_margins",
        "breast_density",
        "subtlety",
        "patient_id",
    ]

    tag_metas = [sly.TagMeta(name.lower(), sly.TagValueType.NONE) for name in tag_names_nontype]
    tag_metas_any = [
        sly.TagMeta(name.lower(), sly.TagValueType.ANY_STRING) for name in tag_names_anystirng
    ]
    tag_metas.extend(tag_metas_any)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[obj_class], tag_metas=tag_metas)
    api.project.update_meta(project.id, meta.to_json())

    dataset_test = api.dataset.create(project.id, "test", change_name_if_conflict=True)
    dataset_train = api.dataset.create(project.id, "train", change_name_if_conflict=True)

    total_files = len(image_test) + len(image_train)

    project_images = {"test": image_test, "train": image_train}
    progress = sly.Progress("Create datasets {}".format("test,train"), total_files)

    for ds in project_images:
        if ds == "test":
            dataset = dataset_test
        else:
            dataset = dataset_train
        img_paths = project_images[ds]
        for img_pathes_batch in sly.batched(img_paths, batch_size=batch_size):
            img_names_batch = [os.path.basename(img_path) for img_path in img_pathes_batch]
            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]
            anns_batch = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)
            progress.iters_done_report(len(img_names_batch))
    return project
