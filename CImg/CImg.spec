Name:           CImg
Version:        1.5.1
Release:        1%{?dist}
Summary:        C++ Template Image Processing Toolkit

License:        CeCILL
URL:            http://cimg.sourceforge.net/
Source0:        http://downloads.sourceforge.net/cimg/%{name}-%{version}.zip

# this patch is in upstream CVS, but not in the distributed sources
Patch1:         CImg-1.5.1-pkgconfig.patch

BuildArch:      noarch
BuildRequires:  texlive-latex, doxygen, libstdc++-devel

%description
%{summary}

%package devel
Summary:        C++ Template Image Processing Toolkit
Group:          Development/Libraries

# -devel subpkg only atm, compat with other distros
Provides:       %{name} = %{version}-%{release}
# not *strictly* a -static pkg, but the results are the same
Provides:       %{name}-static = %{version}-%{release}

Requires:       libstdc++-devel

%description devel
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

# Convert licence files to utf-8
for file in Licence_CeCILL-C_V1-en.txt Licence_CeCILL_V2-en.txt; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

# make documentation
cd html
doxygen CImg.doxygen

# make pdf documentation
cd latex
make
cd ../..

%check
cd examples
# just a quick build test without other libraries
# as there is no configure provided and paths like /usr/lib are hardcoded in the makefile
make mlinux %{?_smp_mflags}

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
install -d %{buildroot}/%{_docdir}/%{name}-devel-%{version}/html
install -p -m 644 html/reference/* %{buildroot}/%{_docdir}/%{name}-devel-%{version}/html
install -p -m 644 html/latex/refman.pdf %{buildroot}/%{_docdir}/%{name}-devel-%{version}/CImg_reference.pdf

%files devel
%defattr(-,root,root,-)
%doc README.txt Licence_CeCILL_V2-en.txt Licence_CeCILL-C_V1-en.txt
# the html and pdf documentation is installed automatically
%dir %{_includedir}/CImg
%{_includedir}/CImg/CImg.h
%{_includedir}/CImg/plugins/
%{_datadir}/pkgconfig/CImg.pc

%changelog
* Thu Aug 30 2012 Gerd v. Egidy <gerd@egidy.de> - 1.5.1-1
- update to current upstream
- fix directory ownership
- update the pkgconfig patch, fix comment
- add check section, compile examples there
- require libstc++-devel: always needed to compile
  the other libraries than can be included are optional

* Wed Aug 29 2012 Gerd v. Egidy <gerd@egidy.de> - 1.5.0-4
- rename to CImg.spec again and create -devel subpackage
  spec snippets for this taken from eigen2.spec
- some cleanups

* Tue Aug 28 2012 Thibault North <tnorth@fedoraproject.org> - 1.5.0-3
- minor fixes

* Sun Aug 26 2012 Gerd v. Egidy <gerd@egidy.de> - 1.5.0-2
- put plugins in separate subdir
- add pkgconfig file (as patch for now, will be submitted upstream)

* Sun Aug 26 2012 Gerd v. Egidy <gerd@egidy.de> - 1.5.0-1
- initial package
