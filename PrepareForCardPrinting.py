# Rename images files for card printing


import os
import re
import shutil
import sys, getopt

# Files to be converted directory (replace '\' with '/')
PROCESS_DIR = ""

# Verso image path
VERSO_IMAGE = ""


IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".bmp", ".tif"]
SUFFIX_RECTO = " - R"
SUFFIX_VERSO = " - V"

def main(argv):

    global PROCESS_DIR
    global VERSO_IMAGE
    
    try:
        opts, args = getopt.getopt(argv,"hd:v:",["help","dir=","verso="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            printHelp()
            sys.exit()
        elif opt in ("-d", "--dir"):
            PROCESS_DIR = arg
        elif opt in ("-v", "--verso"):
            VERSO_IMAGE = arg

    if(not PROCESS_DIR):
        print('Error: directory to process is missing')
        printHelp()
        return

    processRectoFiles(PROCESS_DIR)

    if (VERSO_IMAGE):
        processVersoFile(PROCESS_DIR, VERSO_IMAGE)


def convertToDOSPath(dir):
    return dir.replace("/", "\\")

def convertToPythonPath(dir):
    return dir.replace("\\", "/")
    

def processRectoFiles(processDir):

    # Check directory
    if(not os.path.isdir(processDir)):
        print("ERROR: Directory", processDir, "does not exist")
        os.system("pause")
        exit()
        
    #os.chdir(source_dir)
    print("Processing recto files in", processDir, "...")
    print()

    processDirStr = convertToPythonPath(processDir)
    
    cardSuffixes = [SUFFIX_RECTO, SUFFIX_VERSO]

    # Convert files in directory
    nbTotal  = 0
    nbRenamed = 0
    for dirname, dirnames, filenames in os.walk(processDirStr):

        #print("Processing directory", dirname)
        dirname = convertToDOSPath(dirname)

        # Browse files
        for filename in filenames:

            # Process file given format
            processFile = False
            for format in IMAGE_FORMATS:
                processFile |= (re.search(format, filename) is not None)

            if (processFile):
                nbTotal += 1

                srcFilePath = os.path.join(dirname, filename)
                srcFileName, srcFileExt = os.path.splitext(filename)

                # Do not rename already processed images, ending with " - R" or "- V"

                alreadyProcessed = False
                for suffix in cardSuffixes:
                    alreadyProcessed |= (srcFileName.endswith(suffix))

                if (alreadyProcessed):
                    print("Skipping file", srcFilePath, "...")
                    continue

                # rename image

                dstFileNameExt = srcFileName + SUFFIX_RECTO + srcFileExt
                dstFilePath = os.path.join(dirname, dstFileNameExt)

                print("Renaming file", srcFilePath, "...")
                os.rename(srcFilePath, dstFilePath)
                nbRenamed += 1        

    # Print result
    print()     
    print("Total Files    ", nbTotal)
    print("Renamed Files  ", nbRenamed)


def processVersoFile(processDir, versoFilePath):

    # Check directory
    if(not os.path.isdir(processDir)):
        print("ERROR: Directory", processDir, "does not exist")
        os.system("pause")
        exit()

    # Check directory
    if(not os.path.isfile(versoFilePath)):
        print("ERROR: Verso file", versoFilePath, "does not exist")
        os.system("pause")
        exit()
        
    #os.chdir(source_dir)
    print()
    print()
    print("Copying verso files", versoFilePath, " in", processDir, "...")
    print()

    dstFileName, dstFileExt = os.path.splitext(versoFilePath)

    processDirStr = convertToPythonPath(processDir)

    # Convert files in directory
    nbTotal  = 0
    nbCopied = 0
    for dirname, dirnames, filenames in os.walk(processDirStr):

        #print("Processing directory", dirname)
        dirname = convertToDOSPath(dirname)

        # Browse files
        for filename in filenames:

            # Process file given format
            processFile = False
            for format in IMAGE_FORMATS:
                processFile |= (re.search(format, filename) is not None)

            if (processFile):
                nbTotal += 1

                srcFilePath = os.path.join(dirname, filename)
                srcFileName, srcFileExt = os.path.splitext(filename)

                # process only recto images
                if(not srcFileName.endswith(SUFFIX_RECTO)):
                    print("Skipping", srcFilePath)
                    continue

                # Create verso file path
                srcFileName = srcFileName[:-len(SUFFIX_RECTO)]
                #print("Original file name:", srcFileName)
                dstFileNameExt = srcFileName + SUFFIX_VERSO + dstFileExt
                dstFilePath = os.path.join(dirname, dstFileNameExt)

                # Skip if verso file already exists
                dstFileNameWithSrcExt = srcFileName + SUFFIX_VERSO + srcFileExt
                dstFilePathWithSrcExt = os.path.join(dirname, dstFileNameWithSrcExt)
                if (os.path.isfile(dstFilePath) or os.path.isfile(dstFilePathWithSrcExt)):
                    print("Skipping", dstFilePath)
                    continue

                # Copy verso file
                print("Copying verso file", srcFilePath, "to", dstFilePath, "...")
                shutil.copyfile(versoFilePath, dstFilePath)
                nbCopied += 1

    # Print result
    print()     
    print("Total Files         ", nbTotal)
    print("Copied Verso Files  ", nbCopied)           


def printHelp():
    print()
    print('Usage: python PrepareForCardPrinting.py -d <directory> -v <verso_image_path>')
    print()
    print("Options:")
    print("  -d, --dir <dir>:       directory to bulk rename image files in")
    print("  -v, --verso <rate>:    verso image file path")
    print("  -h, --help:            display help")
    print()


if __name__ == "__main__":
    main(sys.argv[1:])

    # Wait for user input to close program (Windows)
    os.system("pause")
