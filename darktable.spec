#
# RPM Spec for darktable
#
# Based on the Fedora spec, cleaned up for 3.0.0.
#
# Tested on:
#   Fedora Core 30
#

Name:     darktable
Version:  3.0.0
Release:  1%{?dist}
Summary:  Utility to organize and develop raw images
License:  GPLv3+
URL:      https://www.darktable.org


%define namever %{name}-%{version}
%define tarball %{namever}.tar.xz

%define download_url https://github.com/darktable-org/%{name}/releases/download/release-%{version}/%{tarball}

Source0: %{tarball}

BuildRequires: gcc >= 5.0
BuildRequires: sqlite-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: pugixml-devel >= 1.8
BuildRequires: gtk3-devel
BuildRequires: cairo-devel
BuildRequires: lcms2-devel
BuildRequires: exiv2-devel
BuildRequires: libtiff-devel
BuildRequires: libcurl-devel
BuildRequires: libgphoto2-devel
BuildRequires: dbus-glib-devel
BuildRequires: openexr-devel
BuildRequires: libsoup-devel >= 2.4

Requires: sqlite
Requires: libjpeg
Requires: libpng
Requires: pugixml >= 1.8
Requires: gtk3
Requires: cairo
Requires: lcms2
Requires: exiv2
Requires: libtiff
Requires: libcurl
Requires: libgphoto2
Requires: dbus-glib
Requires: fop
Requires: openexr
Requires: libsoup >= 2.4


# ------------------------------------------


# TODO:  Things we _might_ need...
### BuildRequires: clang >= 3.4
### %if 0%{?el7}
### BuildRequires: cmake3 >= 3.10
### %else
### BuildRequires: cmake >= 3.10
### %endif
### BuildRequires: colord-gtk-devel
### BuildRequires: colord-devel
### BuildRequires: cups-devel
### BuildRequires: desktop-file-utils
### # EPEL7 does not have a recent GCC
### %if 0%{?el7}
### BuildRequires: devtoolset-7-toolchain
### BuildRequires: devtoolset-7-libatomic-devel
### %endif
### 
### BuildRequires: flickcurl-devel
### BuildRequires: gcc >= 5.0
### BuildRequires: GraphicsMagick-devel
### BuildRequires: gtk3-devel >= 3.22
### BuildRequires: intltool
### # iso-codes dependency not mandatory, just optional / recommended
### # in future please check if EL7 iso-codes version is >= 3.66
### %if 0%{?fedora}
### BuildRequires: iso-codes >= 3.66
### %endif
### BuildRequires: gettext
### BuildRequires: json-glib-devel
### 
### BuildRequires: lensfun-devel
### BuildRequires: libappstream-glib
### BuildRequires: libcurl-devel >= 7.18.0
### 
### BuildRequires: librsvg2-devel >= 2.26
### BuildRequires: libsecret-devel
### 
### BuildRequires: libwebp-devel
### # Fedora uses Fedora lua, EPEL7 uses bundled lua
### %if 0%{?fedora}
### BuildRequires: lua-devel >= 5.3
### %endif
### BuildRequires: opencl-headers
### BuildRequires: OpenEXR-devel >= 1.6
### BuildRequires: openjpeg2-devel
### BuildRequires: osm-gps-map-devel >= 1.0
### BuildRequires: perl-interpreter
### BuildRequires: pkgconfig >= 0.22
### BuildRequires: po4a
### BuildRequires: /usr/bin/pod2man
### 
### BuildRequires: sqlite-devel
### BuildRequires: zlib-devel >= 1.2.11
### 
### # iso-codes dependency not mandatory, just optional / recommended
### # in future please check if EL7 iso-codes version is >= 3.66
### %if 0%{?fedora}
### Requires: iso-codes >= 3.66
### %endif
### 

# Concerning rawspeed bundled library, see
# https://fedorahosted.org/fpc/ticket/550#comment:9
Provides: bundled(rawspeed)
### %if 0%{?el7}
### Provides: bundled(lua)
### %endif

# uses xmmintrin.h
ExclusiveArch: x86_64 aarch64


%description
Darktable is a virtual light-table and darkroom for photographers:
it manages your digital negatives in a database and lets you view them
through a zoom-able light-table.
It also enables you to develop raw images and enhance them.


%prep

# The usual prep macro doesn't handle .xz files.
tar xJf ${RPM_SOURCE_DIR}/%{tarball}


%build
cd %{namever}
./build.sh --prefix %{_prefix}



%install
%{__make} -C %{namever}/build DESTDIR=%{buildroot} install

%find_lang %{name}
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/darktable.appdata.xml




%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
# TODO: Re-enable these and fix problems
#%license LICENSE
%{_bindir}/darktable
%{_bindir}/darktable-chart
%{_bindir}/darktable-cli
%{_bindir}/darktable-cltest
%{_bindir}/darktable-cmstest
%{_bindir}/darktable-generate-cache
%{_bindir}/darktable-rs-identify
%{_libdir}/darktable
%{_datadir}/darktable
%{_datadir}/applications/darktable.desktop
%{_datadir}/appdata/darktable.appdata.xml
%{_datadir}/icons/hicolor/*/apps/darktable*
%{_docdir}/darktable
%{_mandir}/man1/darktable*.1.gz
%{_mandir}/*/man1/darktable*.1.gz
