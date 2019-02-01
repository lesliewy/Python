import fnmatch
import json
import logging
import os
import time

from db import mongo
from files import file_util

#####
#
# 将生成的财报数据插入db, 这里用mongodb
#
#####
dbname = "stock";
collection_pre = "financial_"
username = "stock"
password = "stock123"
json_dir = "/Users/leslie/MyProjects/GitHub/Python/Stock/data/financial_report/2019/01/30";

# 日志
LOG_FORMAT = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='../log/parse.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def main():
    logging.info("开始插入mongodb....")
    start = time.time()
    for dir in os.listdir(json_dir):
        full_dir = os.path.join(json_dir, dir);
        for file in os.listdir(full_dir):
            if fnmatch.fnmatch(file, "*.json"):
                persis(os.path.join(full_dir, file));
    end = time.time();
    logging.info("==================== 已全部插入mongodb: %f s", (end - start))


def persis(file_full_path):
    json_in_file = json.loads(file_util.read_file(file_full_path));
    collection_post, code = get_collection_code_from_file(file_full_path);
    json_in_file["code"] = code;

    db = get_mongo_db();
    db[collection_pre + collection_post].insert(json_in_file);


def get_collection_code_from_file(file_full_path):
    basename = os.path.basename(file_full_path)
    return basename.partition("_")[0], basename.partition("_")[2].partition(".")[0]


def get_mongo_db():
    return mongo.get_mongo_db(dbname, username, password);


# main();
