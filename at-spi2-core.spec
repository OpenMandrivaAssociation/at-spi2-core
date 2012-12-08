%define major		0
%define gir_major	2.0
%define libname		%mklibname atspi %{major}
%define girname		%mklibname atspi-gir %{gir_major}
%define develname 	%mklibname -d atspi

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Name:		at-spi2-core
Version:	2.6.2
Release:	1
Summary:	Protocol definitions and daemon for D-Bus at-spi
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Source0:	http://ftp.acc.umu.se/pub/GNOME/sources/at-spi2-core/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xevie)

Requires:	dbus

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains libraries used by %{name}.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Summary:	Libraries and include files with %{name}
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package provides the necessary development libraries and include 
files to allow you to develop with %{name}.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static

%make LIBS='-lgmodule-2.0'

%install
%makeinstall_std
find %{buildroot} -name *.la | xargs rm

%find_lang %{name}


%files -f %{name}.lang
%doc COPYING AUTHORS README
%dir %{_sysconfdir}/at-spi2/
%config(noreplace) %{_sysconfdir}/at-spi2/accessibility.conf
%{_sysconfdir}/xdg/autostart/at-spi-dbus-bus.desktop
%{_libexecdir}/at-spi2-registryd
%{_libexecdir}/at-spi-bus-launcher
%{_datadir}/dbus-1/services/org.*.service

%files -n %{libname}
%{_libdir}/libatspi.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Atspi-%{gir_major}.typelib

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/libatspi
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/gir-1.0/Atspi-%{gir_major}.gir



%changelog
* Tue Nov 13 2012 Arkady L. Shane <ashejn@rosalab.ru> 2.6.2-1
- update to 2.6.2

* Tue Oct 30 2012 Arkady L. Shane <ashejn@rosalab.ru> 2.6.1-1
- update to 2.6.1

* Fri Sep 28 2012 Arkady L. Shane <ashejn@rosalab.ru> 2.6.0-1
- update to 2.6.0

* Sat May 05 2012 Alexander Khrukin <akhrukin@mandriva.org> 2.5.1-1
+ Revision: 796621
- version update 2.5.1

* Sat Mar 10 2012 Matthew Dawkins <mattydaw@mandriva.org> 2.2.3-1
+ Revision: 783905
- new version 2.2.3
- split gir pkg
- cleaned up spec

* Tue May 24 2011 Götz Waschk <waschk@mandriva.org> 2.0.2-1
+ Revision: 678052
- update to new version 2.0.2

* Tue Apr 26 2011 Funda Wang <fwang@mandriva.org> 2.0.1-1
+ Revision: 659142
- update to new version 2.0.1

* Tue Apr 05 2011 Funda Wang <fwang@mandriva.org> 2.0.0-1
+ Revision: 650439
- new version 2.0.0

* Tue Nov 16 2010 Götz Waschk <waschk@mandriva.org> 0.4.1-1mdv2011.0
+ Revision: 597921
- update to new version 0.4.1

* Tue Sep 28 2010 Götz Waschk <waschk@mandriva.org> 0.4.0-1mdv2011.0
+ Revision: 581615
- update to new version 0.4.0

* Tue Sep 14 2010 Götz Waschk <waschk@mandriva.org> 0.3.92-1mdv2011.0
+ Revision: 578144
- update to new version 0.3.92

* Tue Aug 31 2010 Götz Waschk <waschk@mandriva.org> 0.3.91-1mdv2011.0
+ Revision: 574617
- new version
- update file list

* Tue Aug 17 2010 Götz Waschk <waschk@mandriva.org> 0.3.90-1mdv2011.0
+ Revision: 570822
- update to new version 0.3.90
- fix source URL

* Thu Jul 29 2010 Götz Waschk <waschk@mandriva.org> 0.3.4-1mdv2011.0
+ Revision: 563123
- new version

* Wed Mar 31 2010 Götz Waschk <waschk@mandriva.org> 0.1.8-1mdv2010.1
+ Revision: 530226
- update to new version 0.1.8

* Fri Feb 19 2010 Götz Waschk <waschk@mandriva.org> 0.1.7-1mdv2010.1
+ Revision: 508298
- new version
- update file list

* Tue Feb 09 2010 Götz Waschk <waschk@mandriva.org> 0.1.6-1mdv2010.1
+ Revision: 502688
- new version
- update file list

* Mon Jan 11 2010 Götz Waschk <waschk@mandriva.org> 0.1.5-1mdv2010.1
+ Revision: 489820
- update to new version 0.1.5

* Mon Dec 28 2009 Frederic Crozat <fcrozat@mandriva.com> 0.1.4-1mdv2010.1
+ Revision: 483107
- import at-spi2-core

