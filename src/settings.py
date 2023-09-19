from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "CBIS-DDSM"
PROJECT_NAME_FULL: str = (
    "Curated Breast Imaging Subset of Digital Database for Screening Mammography"
)
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.CC_BY_4_0()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [
    Industry.Medical(),
    Research.Medical(),
]
CATEGORY: Category = Category.Medical()

CV_TASKS: List[CVTask] = [
    CVTask.InstanceSegmentation(),
    CVTask.ObjectDetection(),
    CVTask.SemanticSegmentation(),
]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_DATE: Optional[str] = " 2017-09-14"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22516629"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 4266633
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/cbis-ddsm"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = [
    "https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22516629#22516629accaef0469834754b89af9e007760b10"
]
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[
    Union[str, List[str], Dict[str, str]]
] = "https://www.nature.com/articles/sdata2017177"
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = {
    "Prepossessed version": "https://www.kaggle.com/datasets/mohamedbenticha/cbis-ddsm"
}

CITATION_URL: Optional[
    str
] = "https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22516629#22516629c81c47058258450fbdab650f04bea8a2"
AUTHORS: Optional[List[str]] = [
    "Rebecca Sawyer Lee",
    "Francisco Gimenez",
    "Assaf Hoogi",
    "Kanae Kawai Miyake",
    "Mia Gorovoy",
    "Daniel L. Rubin",
]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = ["Stanford University"]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = ["https://www.stanford.edu/"]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {
    "Breast": ["left", "right"],
    "View": ["cc", "mlo"],
    "BI-RADS assessment": [
        "assessment:1",
        "assessment:2",
        "assessment:3",
        "assessment:4",
        "assessment:5",
        "assessment:0",
    ],
    "pathology": ["benign", "benign_without_callback", "malignant"],
    "case": ["calcification", "mass"],
    "__POSTTEXT__": "Also dataset includes ***calc_type***, ***calc_distribution***, ***mass_shape***, ***mass_margins***, ***breast_density***, ***subtlety***, ***patient_id*** tags",
}
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
