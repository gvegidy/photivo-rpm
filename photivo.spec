# Tarfile created from Mercurial repository
# hg clone https://photivo.googlecode.com/hg/  %{name}-`date +%Y%m%d`
# cd %{name}-`date +%Y%m%d`
# hg update && rm -rf .hg/
# cd - && tar cf %{name}-`date +%Y%m%d`
# bzip2 %{name}-`date +%Y%m%d`.tar

%define grma_version 1.3.16

Name:		photivo
Version:	20120818
Release:	1%{?dist}
Summary:	RAW photo processor

Group:		Applications/Multimedia 
License:	GPLv3+
URL:		http://www.photivo.org/
Source0:	%{name}-%{version}.tar.bz2
Source1:    http://downloads.sourceforge.net/sourceforge/graphicsmagick/GraphicsMagick-%{grma_version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires: ccache libtool convmv mercurial
BuildRequires: qt-devel exiv2-devel lensfun-devel fftw-devel gimp-devel lcms2-devel bzip2-devel liblqr-1-devel
BuildRequires: libjpeg-devel libtiff-devel libpng-devel libwmf-devel
BuildRequires: desktop-file-utils libjasper-devel libxml2-devel 

%description
Photivo is a free and open source photo processor. 
It handles your RAW files as well as your bitmap files in a non-destructive 
16 bit processing pipe with integrated gimp export and batch mode.

%package -n photivo-gimp
Summary:    GIMP integration for Photivo
Group:      Applications/Multimedia
Requires:   %{name} = %{version}

%description -n photivo-gimp
GIMP integration for Photivo.
Photivo is a free and open source photo processor. 

%prep
%setup -q

sed -i "s|.*shortcut2.*||g" photivo.pro
sed -i "s|QMAKE_POST_LINK=strip \$(TARGET)||g" photivoProject/photivoProject.pro
chmod 0644 Sources/{*.h,*.cpp,*/*.c,*/*.h}

tar xjf %{SOURCE1}
ln -s GraphicsMagick-%{grma_version} GraphicsMagick

%build

# photivo currently statically links a local copy of GraphicsMagick.
# This is because photivo needs GraphicsMagick compiled with lcms2,
# while the common GraphicsMagick is linked with lcms1.
# An upcoming version of GraphicsMagick will always use lcms2, then
# photivo will switch to the common GraphicsMagick.
#
# see http://code.google.com/p/photivo/issues/detail?id=58

# configure and build our own GraphicsMagick
cd GraphicsMagick
%configure --enable-static \
           --with-quantum-depth=16 \
           --without-lcms \
           --with-lcms2 \
           --with-magick_plus_plus \
           --with-modules \
           --with-threads \
           --with-x \
           --with-xml \
           --without-dps \
           --without-gslib \
           --with-windows-font-dir=%{_datadir}/fonts/msttcorefonts \
           --with-gs-font-dir=%{_datadir}/fonts/default/ghostscript
make %{?_smp_mflags}
mkdir install
make DESTDIR=`pwd`/install install
if [ -e install/usr/lib64 ]; then
        mv install/usr/lib64 install/usr/lib
fi

cd ..

# configure photivo
export PKG_CONFIG_PATH=`pwd`/GraphicsMagick/install/usr/lib/pkgconfig/:$PKG_CONFIG_PATH
qmake-qt4 PREFIX=%{_prefix}	QMAKE_CFLAGS="%{optflags}"\
				QMAKE_CXXFLAGS="%{optflags}" \
				QMAKE_LFLAGS="%{optflags}" QMAKE_STRIP=":" 
# adobe profiles and curve creation does not work currently
#                "CONFIG+=WithAdobeProfiles WithCurves"

cd ptClearProject && qmake-qt4 -o Makefile ptClearProject.pro && cd ..
cd ptCreateCurvesProject && qmake-qt4 -o Makefile ptCreateCurvesProject.pro && cd ..
cd photivoProject && qmake-qt4 -o Makefile photivoProject.pro && cd ..
cd ptGimpProject && qmake-qt4 -o Makefile ptGimpProject.pro && cd ..
cd ptCreateAdobeProfilesProject && qmake-qt4 -o Makefile ptCreateAdobeProfilesProject.pro && cd ..

# replace references to GraphicsMagick headers and libraries with our local version
sed -i 's/-I\/usr\/include\/GraphicsMagick/-I..\/GraphicsMagick\/install\/usr\/include\/GraphicsMagick/g' */Makefile
sed -i 's/-lGraphicsMagick++ -lGraphicsMagickWand -lGraphicsMagick/..\/GraphicsMagick\/install\/usr\/lib\/libGraphicsMagick++.a ..\/GraphicsMagick\/install\/usr\/lib\/libGraphicsMagickWand.a ..\/GraphicsMagick\/install\/usr\/lib\/libGraphicsMagick.a -lpng -lxml2 -ltiff -lwmf -lwmflite -ljasper -lz -lfreetype -lX11 -lXext -lbz2/g' */Makefile

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
