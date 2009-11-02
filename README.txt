*************************************************************************
*                                                                       *
*                              Unum 4.0                                 *
*                           Units in Python                             *
*                                                                       *
*                      (c) 2000-2003 Pierre Denis                       *
*                                                                       *
*************************************************************************

-------------------------------------------------------------------------
* Prerequisite : 
-------------------------------------------------------------------------

  - platform : any (Unum is a pure Python package, hence the portablity
               is presumed to be high)
  - Python 2.2 or higher installed

-------------------------------------------------------------------------
* To install Unum 4.0 :
-------------------------------------------------------------------------

  - unzip Unum installation files in <your-install-directory>
  - cd <your-install-directory>/Unum-4.0
  - python setup.py install
    this will install Unum packages in your Python site-packages directory
    i.e. it will create the directory <python-site-packages-dir>/unum 
  - if the installation is successful (see below),
    you can safely remove <your-install-directory>

-------------------------------------------------------------------------
* To run the test cases :
-------------------------------------------------------------------------

 (usage : installation check-up, non-regression tests)
  - change directory to <python-site-packages-dir>/unum/tools
  - type the following:
   	python test.py
    A couple of lines should report the results of the test cases 
    Note : depending on your platform, some spurious errors may be
           reported due to numerical precision issues

-------------------------------------------------------------------------
* Other information :
-------------------------------------------------------------------------

  - E-mail : pierre.denis@spacebel.be
  (for questions, comments, bug report, etc)  

  - Unum site : http://home.tiscali.be/be052320/Unum.html  
  (for a comprehensive tutorial, papers, etc)


=========================================================================