# -*- coding:utf-8 -*-

# import download.persist
from download import persist
import os

MATCH_URL_PRE = "http://www.okooo.com/danchang/"

DOWNLOAD_DIR = "/Users/leslie/MyProjects/Data/Okooo"

DOWNLOAD_MATCH_DIR = "/Users/leslie/MyProjects/Data/Okooo/match"


def download_match(match_term):
    match_term_dir = DOWNLOAD_MATCH_DIR + match_term
    if (not os.path.exists(match_term_dir)):
        os.makedirs(match_term_dir)
    persist.persist_file(MATCH_URL_PRE + match_term, match_term_dir, "utf-8")


def test_download_match():
    match_term = "180504"
    download_match(match_term)


test_download_match()
