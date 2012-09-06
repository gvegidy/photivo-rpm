# Tarfile created from Mercurial repository
# hg clone https://photivo.googlecode.com/hg/  %{name}-`date +%Y%m%d`
# cd %{name}-`date +%Y%m%d`
# hg update && rm -rf .hg/
# cd - && tar cf %{name}-`date +%Y%m%d`
# bzip2 %{name}-`date +%Y%m%d`.tar

Name:		photivo
Version:	20120906
Release:	1%{?dist}
Summary:	RAW photo processor

Group:		Applications/Multimedia 
License:	GPLv3+
URL:		http://www.photivo.org/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires: ccache libtool convmv
BuildRequires: qt-devel exiv2-devel lensfun-devel fftw-devel gimp-devel lcms2-devel bzip2-devel liblqr-1-devel
BuildRequires: libjpeg-devel libtiff-devel libpng-devel libwmf-devel
BuildRequires: desktop-file-utils libjasper-devel libxml2-devel CImg-devel

# beginning with this version GM links with lcms2
Requires: GraphicsMagick >= 1.3.16-5
BuildRequires: GraphicsMagick-devel >= 1.3.16-5
BuildRequires: GraphicsMagick-c++-devel >= 1.3.16-5

%description
Photivo is a free and open source photo processor. 
It handles your RAW files as well as your bitmap files in a non-destructive 
16 bit processing pipe with integrated gimp export and batch mode.

%package -n photivo-gimp
Summary:    GIMP integration for Photivo
Group:      Applications/Multimedia
Requires:   %{name} = %{version}
Requires:   gimp

%description -n photivo-gimp
GIMP integration for Photivo.
Photivo is a free and open source photo processor. 

%prep
%setup -q

sed -i "s|.*shortcut2.*||g" photivo.pro
sed -i "s|QMAKE_POST_LINK=strip \$(TARGET)||g" photivoProject/photivoProject.pro
chmod 0644 Sources/{*.h,*.cpp,*/*.c,*/*.h}

# set our version, don't rely on hg
sed -i "s|APPVERSION = .*|APPVERSION = %{version}-%{release}|g" photivoProject/photivoProject.pro

# we don't use the local copy of CImg, delete it to make sure it doesn't accidentally slip back in
rm -f Sources/greyc/CImg.h

%build

# configure photivo
export PKG_CONFIG_PATH=`pwd`/GraphicsMagick/install/usr/lib/pkgconfig/:$PKG_CONFIG_PATH
qmake-qt4 PREFIX=%{_prefix}	QMAKE_CFLAGS="%{optflags}"\
                QMAKE_CXXFLAGS="%{optflags}" \
                QMAKE_LFLAGS="%{optflags}" QMAKE_STRIP=":" \
                "CONFIG+=WithSystemCImg"
# adobe profiles and curve creation does not work currently
#                "CONFIG+=WithAdobeProfiles WithCurves"

# build photivo
make	%{?_smp_mflags}    

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot} 
mkdir -p %{buildroot}/%{_bindir}

install -p -m 755 ptClear %{buildroot}/%{_bindir}

# Fix perms for lensfun
chmod 0644 $RPM_BUILD_ROOT/%{_datadir}/%{name}/LensfunDatabase/*.xml
chmod 0644 $RPM_BUILD_ROOT/%{_datadir}/%{name}/ChannelMixers/*.ptm

# Fix perms 
chmod 0644 README COPYING
sed -i "s|\r||g" README

desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop

# install gimp plugin
mkdir -p %{buildroot}%{_libdir}/gimp/2.0/plug-ins
install -m 755 -p ptGimp %{buildroot}%{_libdir}/gimp/2.0/plug-ins/
install -m 755 -p mm\ extern\ photivo.py %{buildroot}%{_libdir}/gimp/2.0/plug-ins/

%files
%doc COPYING README
%{_bindir}/photivo
%{_bindir}/ptClear
%{_datadir}/photivo
%{_datadir}/applications/photivo.desktop
%{_datadir}/pixmaps/photivo-appicon.png

%files -n photivo-gimp
%defattr(-,root,root)
"%{_libdir}/gimp/2.0/plug-ins/mm extern photivo.py"
"%{_libdir}/gimp/2.0/plug-ins/mm extern photivo.pyc"
"%{_libdir}/gimp/2.0/plug-ins/mm extern photivo.pyo"
%{_libdir}/gimp/2.0/plug-ins/ptGimp

%changelog
* Thu Sep 06 2012 Gerd v. Egidy <gerd@egidy.de> - 20120906-1
- update to current upstream
- patch to use system supplied CImg has been applied upstream
- patch for CImg 1.5.0+ support has been applied upstream
- the gimp plugin obviously requires gimp
- fix build dependencies

* Mon Aug 27 2012 Gerd v. Egidy <gerd@egidy.de> - 20120818-3
- Improve configuring with qmake
- Insert rpm version into the program, don't rely on hg for this anymore
- add patch to use a system supplied CImg instead of the local copy
- add patch to compile with CImg version 1.5.0

* Thu Aug 23 2012 Gerd v. Egidy <gerd@egidy.de> - 20120818-2
- GraphicsMagick now links against lcms2 (#849778)
- Remove our local copy of GraphicsMagick and link against the system one

* Sat Aug 18 2012 Thibault North <tnorth@fedoraproject.org> - 20120818-1
- Small fixes

* Thu Aug 16 2012 Gerd v. Egidy <gerd@egidy.de> - 20120816-1
- update to upstream 20120816-1
- statically link our own GraphicsMagick
  Idea and parts of the code from Sergey Salnikov <salsergey@gmail.com>
- sub-package for the gimp plugin

* Fri Nov 25 2011 Thibault North <tnorth@fedoraproject.org> - 20111125-1
- Sync upstream

* Wed Apr 27 2011 Thibault North <tnorth@fedoraproject.org> - 20110427-1
- Initial package
