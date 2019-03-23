import requests
from pathlib import Path
from tqdm import tqdm
import zipfile
from normalizers import NormalizerEN, NormalizerAR

def resume_download(fileurl, resume_byte_pos):
    resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
    return requests.get(fileurl, headers=resume_header, stream=True,  verify=False, allow_redirects=True)

def downloadFile(url, targetPath):

    path = Path(targetPath)
    resume_byte_pos = 0 if not path.is_file() else path.stat().st_size
    with resume_download(url, resume_byte_pos) as r:
        
        with open(targetPath, 'ab') as f:
            total_size = int(r.headers.get('content-length'))
            chunk_size = 8192
            for chunk in tqdm(iterable = r.iter_content(chunk_size = chunk_size), total = total_size//chunk_size, unit = 'KB'):
                if chunk:
                    f.write(chunk)

        r.close()

# TODO: optimization - check if files are already extracted an match in size ones in the archive.
def extractFile(filePath, targetDir):
    print("Uncompressing %s" % filePath)
    zf = zipfile.ZipFile(filePath, 'r')
    uncompress_size = sum((f.file_size for f in zf.infolist()))
    extracted_size = 0

    for f in zf.infolist():
        extracted_size += f.file_size
        print("%s %%\r" % (extracted_size * 100/uncompress_size))
        zf.extract(f, targetDir)
    
    filesList = zf.namelist()
    zf.close()
    return filesList

def splitTrainValidationTest(filePath, testLineCount, validLineCount, normalizer):

    srcFileName = filePath.parents[0].joinpath("src" + filePath.name)
    vldFileName = filePath.parents[0].joinpath("vld" + filePath.name)
    tstFileName = filePath.parents[0].joinpath("tst" + filePath.name)

    with open(filePath, 'rt', encoding = "utf-8") as f:

        f_enumerator = enumerate(f)

        with open(tstFileName, 'wt', encoding = "utf-8") as tst_f:
            for i, line in f_enumerator:
                #------------------------------------
                normalizer.NormalizeLine(line) #skip: write test sentences as is. (TODO: for now!)
                #------------------------------------
                tst_f.write(line)
                if i > testLineCount - 2:
                    break

        with open(vldFileName, 'wt', encoding = "utf-8") as vld_f:
            for i, line in f_enumerator:
                #------------------------------------
                line = normalizer.NormalizeLine(line)
                #------------------------------------
                vld_f.write(line)
                if i > testLineCount + validLineCount - 2:
                    break

        with open(srcFileName, 'wt', encoding = "utf-8") as src_f:
            for i, line in f_enumerator:
                #------------------------------------
                line = normalizer.NormalizeLine(line)
                #------------------------------------
                src_f.write(line)

    vcbFileName = filePath.parents[0].joinpath("vcb" + filePath.name)
    normalizer.SaveVocab(vcbFileName)

    return i > testLineCount + validLineCount

def fetchDataSplit(url, saveAs, expandTo, validationCount, testCount):
    downloadFile(url, saveAs)
    fileList = extractFile(saveAs, expandTo)
    for fileName in fileList:
        filePath = Path(expandTo).joinpath(fileName)
        if filePath.suffix == ".en":
            success = splitTrainValidationTest(filePath, validationCount, testCount, NormalizerEN())
            print("Data split for %s was successful? %r" % (filePath.as_posix(), success))
        if filePath.suffix == ".ar":
            success = splitTrainValidationTest(filePath, validationCount, testCount, NormalizerAR())
            print("Data split for %s was successful? %r" % (filePath.as_posix(), success))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', help='Specify dataset to fetch and prepare')
    args = parser.parse_args()

    if args.dataset == "TED2013":
        fetchDataSplit("http://opus.nlpl.eu/download.php?f=TED2013/v1.1/moses/ar-en.txt.zip",
            "Data/Ted2013.zip", "Data/Ted2013", 
            5000, 1000)

    if args.dataset == "OpenSubtitle2016":
        fetchDataSplit("http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2016/moses/ar-en.txt.zip",
            "Data/OpenSubtitle2016.zip", "Data/OpenSubtitle2016", 
            5000, 1000)
