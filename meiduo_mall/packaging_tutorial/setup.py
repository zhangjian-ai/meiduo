import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DingTalkLoginTool",
    version="0.0.2",
    author="jian.zhang",
    author_email="zj19180525254@163.com",
    description="DingTalkLoginTool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhangjian-ai/meiduo/tree/master/meiduo_mall/meiduo_mall/utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# 在当前目录下打包并上传
# python3 setup.py sdist
# python3 setup.py sdist upload
