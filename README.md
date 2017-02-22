# How to setup boto3 + virtualenv on Mac OSX

Step 1 - Verify whether we already have virtualenv or not.
~ SaiLinnThu$ pip list
pip (8.1.1)
setuptools (20.10.1)
vboxapi (1.0)

Step 2 - Install virtualenv.
~ SaiLinnThu$ pip install virtualenv                         > pip uninstall virtualenv
Collecting virtualenv
  Downloading virtualenv-15.1.0-py2.py3-none-any.whl (1.8MB)
    100% |████████████████████████████████| 1.8MB 519kB/s 
Installing collected packages: virtualenv
Successfully installed virtualenv-15.1.0

Step 3 - Verify virtualenv.
~ SaiLinnThu$ pip list
pip (8.1.1)
setuptools (20.10.1)
vboxapi (1.0)
virtualenv (15.1.0)

Step 4 - Create a folder my-virtual-environments.
~ SaiLinnThu$ mkdir my-virtual-environments
~ SaiLinnThu$ cd my-virtual-environments

Step 5 - Create a virtual environment called boto3_env.
my-virtual-environments SaiLinnThu$ virtualenv boto3_env
New python executable in /Users/sailinnthu/my-virtual-environments/boto3_env/bin/python
Installing setuptools, pip, wheel...done.

Step 6 - Activate boto3_env.
my-virtual-environments SaiLinnThu$ source boto3_env/bin/activate
(boto3_env) 192-168-1-6:my-virtual-environments SaiLinnThu$

Step 7 - Git clone boto3.
(boto3_env) 192-168-1-6:my-virtual-environments SaiLinnThu$ git clone https://github.com/boto/boto3.git
Cloning into 'boto3'...
remote: Counting objects: 5171, done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 5171 (delta 0), reused 0 (delta 0), pack-reused 5166
Receiving objects: 100% (5171/5171), 1.19 MiB | 157.00 KiB/s, done.
Resolving deltas: 100% (3383/3383), done.
Checking connectivity... done.

Step 8 - Browse /Users/sailinnthu/my-virtual-environments.  We will find a folder called "boto3"

Step 9 - Change to "boto3" directory.
(boto3_env) 192-168-1-6:my-virtual-environments SaiLinnThu$ cd boto3
(boto3_env) 192-168-1-6:boto3 SaiLinnThu$

Step 10 - Create another virtualenv called "venv".
(boto3_env) 192-168-1-6:boto3 SaiLinnThu$ virtualenv venv
New python executable in /Users/sailinnthu/my-virtual-environments/boto3/venv/bin/python
Installing setuptools, pip, wheel...done.

Step 11 - Activate "venv".
(boto3_env) 192-168-1-6:boto3 SaiLinnThu$ . venv/bin/activate
(venv) 192-168-1-6:boto3 SaiLinnThu$

Step 12 - Setup/Install "boto3" Development. ( pip install -r requirements.txt && pip install -e .)
(venv) 192-168-1-6:boto3 SaiLinnThu$ pip install -r requirements.txt
Ignoring unittest2: markers 'python_version == "2.6"' don't match your environment
Obtaining botocore from git+git://github.com/boto/botocore.git@develop#egg=botocore (from -r requirements.txt (line 1))
  Cloning git://github.com/boto/botocore.git (to develop) to ./venv/src/botocore
Obtaining jmespath from git+git://github.com/boto/jmespath.git@develop#egg=jmespath (from -r requirements.txt (line 2))
  Cloning git://github.com/boto/jmespath.git (to develop) to ./venv/src/jmespath
Obtaining s3transfer from git+git://github.com/boto/s3transfer.git@develop#egg=s3transfer (from -r requirements.txt (line 3))
  Cloning git://github.com/boto/s3transfer.git (to develop) to ./venv/src/s3transfer
Collecting nose==1.3.3 (from -r requirements.txt (line 4))
  Downloading nose-1.3.3.tar.gz (274kB)
    100% |████████████████████████████████| 276kB 1.4MB/s 
Collecting mock==1.3.0 (from -r requirements.txt (line 5))
  Downloading mock-1.3.0-py2.py3-none-any.whl (56kB)
    100% |████████████████████████████████| 61kB 2.7MB/s 
Collecting wheel==0.24.0 (from -r requirements.txt (line 6))
  Downloading wheel-0.24.0-py2.py3-none-any.whl (63kB)
    100% |████████████████████████████████| 71kB 1.7MB/s 
Collecting python-dateutil<3.0.0,>=2.1 (from botocore->-r requirements.txt (line 1))
  Downloading python_dateutil-2.6.0-py2.py3-none-any.whl (194kB)
    100% |████████████████████████████████| 194kB 1.6MB/s 
Collecting docutils>=0.10 (from botocore->-r requirements.txt (line 1))
  Downloading docutils-0.13.1-py2-none-any.whl (537kB)
    100% |████████████████████████████████| 542kB 1.2MB/s 
Collecting futures<4.0.0,>=2.2.0 (from s3transfer->-r requirements.txt (line 3))
  Downloading futures-3.0.5-py2-none-any.whl
Collecting pbr>=0.11 (from mock==1.3.0->-r requirements.txt (line 5))
  Downloading pbr-1.10.0-py2.py3-none-any.whl (96kB)
    100% |████████████████████████████████| 102kB 2.0MB/s 
Collecting funcsigs; python_version < "3.3" (from mock==1.3.0->-r requirements.txt (line 5))
  Downloading funcsigs-1.0.2-py2.py3-none-any.whl
Requirement already satisfied: six>=1.7 in ./venv/lib/python2.7/site-packages (from mock==1.3.0->-r requirements.txt (line 5))
Building wheels for collected packages: nose
  Running setup.py bdist_wheel for nose ... done
  Stored in directory: /Users/sailinnthu/Library/Caches/pip/wheels/08/0f/8e/b708bce2c048c92e55f603f4331e393bfb9596823544ebab6e
Successfully built nose
Installing collected packages: jmespath, python-dateutil, docutils, botocore, futures, s3transfer, nose, pbr, funcsigs, mock, wheel
  Running setup.py develop for jmespath
  Running setup.py develop for botocore
  Running setup.py develop for s3transfer
  Found existing installation: wheel 0.29.0
    Uninstalling wheel-0.29.0:
      Successfully uninstalled wheel-0.29.0
Successfully installed botocore docutils-0.13.1 funcsigs-1.0.2 futures-3.0.5 jmespath mock-1.3.0 nose-1.3.3 pbr-1.10.0 python-dateutil-2.6.0 s3transfer wheel-0.24.0
(venv) 192-168-1-6:boto3 SaiLinnThu$ pip install -e .
Obtaining file:///Users/sailinnthu/my-virtual-environments/boto3
Requirement already satisfied: botocore<1.6.0,>=1.5.0 in ./venv/src/botocore (from boto3==1.4.4)
Requirement already satisfied: jmespath<1.0.0,>=0.7.1 in ./venv/src/jmespath (from boto3==1.4.4)
Requirement already satisfied: s3transfer<0.2.0,>=0.1.10 in ./venv/src/s3transfer (from boto3==1.4.4)
Requirement already satisfied: python-dateutil<3.0.0,>=2.1 in ./venv/lib/python2.7/site-packages (from botocore<1.6.0,>=1.5.0->boto3==1.4.4)
Requirement already satisfied: docutils>=0.10 in ./venv/lib/python2.7/site-packages (from botocore<1.6.0,>=1.5.0->boto3==1.4.4)
Requirement already satisfied: futures<4.0.0,>=2.2.0 in ./venv/lib/python2.7/site-packages (from s3transfer<0.2.0,>=0.1.10->boto3==1.4.4)
Requirement already satisfied: six>=1.5 in ./venv/lib/python2.7/site-packages (from python-dateutil<3.0.0,>=2.1->botocore<1.6.0,>=1.5.0->boto3==1.4.4)
Installing collected packages: boto3
  Running setup.py develop for boto3
Successfully installed boto3
(venv) 192-168-1-6:boto3 SaiLinnThu$

Step 13 - Let's start writing Python. ( we have two buckets in S3. )
(venv) 192-168-1-6:boto3_env SaiLinnThu$ python
Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 26 2016, 12:10:39) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import boto3
>>> s3=boto3.resource('s3')
>>> buckets=s3.buckets.all()
>>> for bucket in buckets:
...     print bucket.name
... 
cloudrhc
vcloudynet
>>> exit()
(venv) 192-168-1-6:boto3_env SaiLinnThu$ deactivate

REFERENCE :
$ pip install virtualenv
$ pip list
$ mkdir Environments
$ cd !$

$ virtualenv project1_env
$ source project1_env/bin/activate

$ which python
$ which pip

$ pip list
$ deactivate

Python Tutorial: virtualenv and why you should use virtual environments > https://www.youtube.com/watch?v=N5vscPTWKOk
Setting up a Python Dev Env in Eclipse > https://www.youtube.com/watch?v=NDFbXIiqT4o
