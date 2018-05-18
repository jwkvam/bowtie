#!/bin/sh

#convert -density 256x256 -background transparent bowtie.svg -define icon:auto-resize -colors 256 favicon.ico

mogrify -format ico -density 600 -define icon:auto-resize=128,64,48,32,16 bowtie.svg



