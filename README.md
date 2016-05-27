Unum 4.2 - Units in Python 
=========================================
&copy; 2000-2003 Pierre Denis<br/>
&copy; 2009-2010 Chris MacLeod<br/>
&copy; 2016      Leszek Trzemecki<br/>

Prerequisites: 
-------------------------------------------------------------------------

  - Python 2.2 or higher. Python 3.x should work as well, but please
    report any bugs.

To install Unum:
-------------------------------------------------------------------------
### Using pip:
  If you have not git yet, install it from https://git-scm.com/downloads
  ```{r, engine='bash', count_lines}
    pip install git+git://github.com/trzemecki/Unum.git
  ```
### Alternatively:
  unzip Unum installation files to any directory.
  ```{r, engine='bash', count_lines}
    cd <install-directory>
    python setup.py install
  ```
  this will install Unum packages in your Python site-packages directory
  i.e. it will create the directory &lt;python-site-packages-dir&gt;/unum 
  if the installation is successful (see below),
  you can safely remove &lt;your-install-directory&gt;

To run the test cases:
-------------------------------------------------------------------------
```{r, engine='bash', count_lines}
  cd <install-directory>
  python setup.py test
```
Other information :
-------------------------------------------------------------------------

  - This repository is cloned from: http://bitbucket.org/kiv/unum/
  - New features in this version:
    - now it is possible to using **sum** funciton with Unum
    - append mechanical units like kN, kPa, kNm
