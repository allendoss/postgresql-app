# Tests
import bucket_downloader
import pytest

def test_createFolder():
    bucket_downloader.createFolder('/home/allen/')
    bucket_downloader.createFolder('/home/allen/output')
    bucket_downloader.createFolder('output')
    bucket_downloader.createFolder('')

def test_bucketFileDownloader():
    pass