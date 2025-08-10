#!/bin/bash
# set -e

INPUT_FILE="$1"

CLI_PREFIX='shell: '
BOLD_RED='\e[1;31m'
NC='\e[0m'

if [ ! -f "$INPUT_FILE" ]; then
    printf "${CLI_PREFIX}${BOLD_RED}Input file '$INPUT_FILE' does not exist. Exiting ... ${NC}\n"
    exit 1
fi

STYLE="${2:-light}"
OUTPUT_PATH="${3:-$(dirname "$INPUT_FILE")}"
CHECK_ONLY="${4:-false}"
PLANTUML_CONTAINER="${5:-plantuml/plantuml:latest}"

INPUT_NAME="$(basename "$INPUT_FILE")"
INPUT_PATH=$(dirname "$INPUT_FILE")
OUTPUT_NAME="${INPUT_NAME%.*}.png"
OUTPUT_NAME_FULL="${INPUT_NAME%.*}-${STYLE}.png"

BASE_CMD="docker run --rm \
    -v \"$(pwd)/${INPUT_PATH}\":/data \
    -e PLANTUML_SECURITY_PROFILE=\"ALLOWLIST\" \
    -e PLANTUML_INCLUDE_PATH=\"/data\" \
    \"${PLANTUML_CONTAINER}\" \
    -DSTYLE=\"${STYLE}\" \
    -o \"/data\""

if [ "$CHECK_ONLY" = true ]; then
    eval "$BASE_CMD -v -checkonly \"/data/${INPUT_NAME}\""
else
    eval "$BASE_CMD \"/data/${INPUT_NAME}\""
fi

# If the desired output path is different from where the file was generated, move it.
printf "${CLI_PREFIX}${BOLD_RED}Renaming and moving ${OUTPUT_NAME_FULL} to ${OUTPUT_PATH} ...${NC}\n"
mv "${INPUT_PATH}/${OUTPUT_NAME}" "${OUTPUT_PATH}/${OUTPUT_NAME_FULL}"