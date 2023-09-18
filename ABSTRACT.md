Published research results are difficult to replicate due to the lack of a standard evaluation data set in the area of decision support systems in mammography; most computer-aided diagnosis (CADx) and detection (CADe) algorithms for breast cancer in mammography are evaluated on private data sets or on unspecified subsets of public databases. This causes an inability to directly compare the performance of methods or to replicate prior results. Authors seek to resolve this substantial challenge by releasing an updated and standardized version of the Digital Database for Screening Mammography (DDSM) for evaluation of future CADx and CADe systems (sometimes referred to generally as CAD) research in mammography. Author's data set, the **CBIS-DDSM** (Curated Breast Imaging Subset of DDSM), includes decompressed images, data selection and curation by trained mammographers, updated mass segmentation and bounding boxes, and pathologic diagnosis for training data, formatted similarly to modern computer vision data sets. The data set contains 753 calcification cases and 891 mass cases, providing a data-set size capable of analyzing decision support systems in mammography.

The DDSM is a collection of mammograms from the following sources: Massachusetts General Hospital, Wake Forest University School of Medicine, Sacred Heart Hospital, and Washington University of St Louis School of Medicine. The DDSM was developed through a grant from the DOD Breast Cancer Research Program, US Army Research and Material Command, and the necessary patient consents were obtained by the original developers of the [DDSM](http://marathon.csee.usf.edu/Mammography/software/HeathEtAlIWDM_2000.pdf). The cases are annotated with ROIs for calcifications and masses, as well as the following information that may be useful for CADe and CADx algorithms: Breast Imaging Reporting and Data System (BI-RADS) descriptors for mass shape, mass margin, calcification type, calcification distribution, and breast density; overall BI-RADS assessment from 0 to 5; rating of the subtlety of the abnormality from 1 to 5; and patient age.

## Mass segmentation

Mass margin and shape have long been proven substantial indicators for diagnosis in mammography. Because of this, many methods are based on developing mathematical descriptions of the tumor outline. Due to the dependence of these methods on accurate ROI segmentation and the imprecise nature of many of the DDSM-provided annotations, as seen in Fig. 2, we applied a lesion segmentation algorithm (described below) that is initialized by the general original DDSM contours but is able to supply much more accurate ROIs. Figure 2 contains example ROIs from the DDSM, our mammographer, and the automated segmentation algorithm. As shown, the DDSM outlines provide only a general location and not a precise mass boundary. The segmentation algorithm was designed to provide exact delineation of the mass from the surrounding tissue. This segmentation was done only for masses and not calcifications.

![Fig.2](https://i.ibb.co/xqKRrDV/41597-2017-Article-BFsdata2017177-Fig2-HTML.webp)
<i>Figure 2: Example ROI outlines from each of the four BI-RADS density categories.</i>

## Standardized train/test splits

Separate sets of cases for training and testing algorithms are important for ensuring that all researchers are using the same cases for these tasks. Specifically, the test set should contain cases of varying difficulty in order to ensure that the method is tested thoroughly. The data were split into a training set and a testing set based on the BI-RADS category. This allows for an appropriate stratification for researchers working on CADe as well as CADx. Note that many of the BI-RADS assessments likely were updated after additional information was gathered by the physician, as it is unconventional to subscribe BI-RADS 4 and 5 to screening images. The split was obtained using 20% of the cases for testing and the rest for training. The data were split for all mass cases and all calcification cases separately. Here ‘case’ is used to indicate a particular abnormality, seen on the craniocaudal (CC) and/or mediolateral oblique (MLO) views, which are the standard views for screening mammography. Figure 3 displays the histograms of BI-RADS assessment and pathology for the training and test sets for calcification cases and mass cases. As shown, the data split was performed in such a way to provide equal level of difficulty in the training and test sets. Table 3 contains the number of benign and malignant cases for each set.

![Fig.3](https://i.ibb.co/wdf4p5n/41597-2017-Article-BFsdata2017177-Fig3-HTML.webp)
<i>Figure 3: Histograms showing distribution of reading difficulty for training and test sets.</i>

![Table 3](https://i.ibb.co/YXP5zzz/Screenshot-2023-09-18-190003.png)
<i>Table 3 Number of Cases and Abnormalities in the Training and Test Sets.</i>

## Data Records

[The original images](https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=22516629#22516629accaef0469834754b89af9e007760b10) are distributed at the full mammography and abnormality level as DICOM files. Full mammography images include both MLO and CC views of the mammograms. 

Metadata for each abnormality was transferred from the original csv files to tag format. For example:

- Patient ID: the first 7 characters of images in the case file

- Density category

- Breast: Left or Right

- View: CC or MLO

- Mass shape (when applicable)

- Mass margin (when applicable)

- Calcification type (when applicable)

- Calcification distribution (when applicable)

- BI-RADS assessment

- Pathology: Benign, Benign without call-back, or Malignant

Please note that the image data for this collection is structured such that each participant has multiple patient IDs.  For example, participant 00038 has 10 separate patient IDs which provide information about the scans within the IDs (e.g. Calc-Test_P_00038_LEFT_CC, Calc-Test_P_00038_RIGHT_CC_1).  This makes it appear as though there are 6,671 patients according to the DICOM metadata, but there are only 1,566 actual participants in the cohort.
