Name:           CImg
Version:        1.5.0
Release:        2%{?dist}
Summary:        C++ Template Image Processing Toolkit

License:        CeCILL v2.0
URL:            http://cimg.sourceforge.net/
Source0:        http://downloads.sourceforge.net/cimg/%{name}-%{version}.zip
Patch1:         CImg-1.5.0-pkgconfig.patch

BuildArch:      noarch
BuildRequires:  texlive-latex, doxygen

%description
The CImg Library is a small, open source, C++ toolkit for image processing.

CImg defines classes and methods to manage images in your own C++ code. 
You can use it to load/save various file formats, access pixel values, 
display/transform/filter images, draw primitives (text, faces, curves, 
3d objects, ...), compute statistics, manage user interactions on images,
and so on...

%prep
%setup -q
%patch1 -p1

%build

# make documentation
cd html
doxygen CImg.doxygen

# make pdf documentation
cd latex
make
cd ../..

%install
rm -rf $RPM_BUILD_ROOT

# install headers
install -d %{buildroot}/%{_includedir}/CImg
install -p -m 644 CImg.h %{buildroot}/%{_includedir}/CImg
install -d %{buildroot}/%{_includedir}/CImg/plugins
install -p -m 644 plugins/* %{buildroot}/%{_includedir}/CImg/plugins

# install pkgconfig file
install -d %{buildroot}/%{_datadir}/pkgconfig
install -p -m 644 resources/CImg.pc %{buildroot}/%{_datadir}/pkgconfig

# install documentation
install -d %{buildroot}/%{_docdir}/%{name}-%{version}/html
install -p -m 644 html/reference/* %{buildroot}/%{_docdir}/%{name}-%{version}/html
install -p -m 644 html/latex/refman.pdf %{buildroot}/%{_docdir}/%{name}-%{version}/CImg_reference.pdf

%files
%defattr(-,root,root,-)
%doc README.txt Licence_CeCILL_V2-en.txt Licence_CeCILL-C_V1-en.txt
# the html and pdf documentation is installed automatically
%{_includedir}/CImg/CImg.h
%{_includedir}/CImg/plugins/
%{_datadir}/pkgconfig/CImg.pc

%changelog
* Sun Aug 26 2012 Gerd v. Egidy <gerd@egidy.de> - 1.5.0-2
- put plugins in separate subdir
- add pkgconfig file (as patch for now, will be submitted upstream)

* Sun Aug 26 2012 Gerd v. Egidy <gerd@egidy.de> - 1.5.0-1
- initial package
