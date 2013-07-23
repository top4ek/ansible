#!/bin/bash

UnsortedDir="/mnt/RAID/Photos/Unsorted"
DestinationDir="/mnt/RAID/Photos"

for strFile in $UnsortedDir/*
    do
        strExt=${strFile##*\.}
        case ${strExt,,} in
                jpg) echo -n "${strFile}: Вроде как фотка..."
                        strEXIFDate=`LC_ALL=POSIX exiv2 pr ${strFile} | \\
            awk '/Image timestamp :/ {printf $4}' | sed 's/:/\//g'`
                        echo -n "Щёлкнуто ${strEXIFDate}..."
                ;;
                mov) echo -n "${strFile}: Вроде как видяха..."
                        strEXIFDate=`LC_ALL=POSIX mediainfo \\
             --Inform="Video;%Encoded_Date%" ${strFile} | awk '{print $2}'| sed 's/-/\//g'`
                        echo -n "Снято ${strEXIFDate}..."
                ;;
                *) echo " ${strFile}: Хз, шо цэ такэ, не буду трогать."
                        continue
                ;;
        esac
        if [ ! -d "${DestinationDir}/${strEXIFDate}" ]; then
                echo -n "Директории нетуть - создаём."
                mkdir -p ${DestinationDir}/${strEXIFDate}
        fi
        echo "Переносим..."
        mv ${strFile} ${DestinationDir}/${strEXIFDate}/
done
