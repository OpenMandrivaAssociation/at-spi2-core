%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define major	0
%define api	2.0
%define libname	%mklibname atspi %{major}
%define girname	%mklibname atspi-gir %{api}
%define devname	%mklibname -d atspi
%bcond_with	bootstrap
%bcond_with	gtkdoc

Summary:	Protocol definitions and daemon for D-Bus at-spi
Name:		at-spi2-core
Version:	2.34.0
Release:	2
Epoch:		1
Group:		System/Libraries
License:	LGPLv2+
Url:		http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Source0:	http://ftp.gnome.org/pub/GNOME/sources/at-spi2-core/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	dbus
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xevie)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(xkbcommon-x11)
BuildRequires:	meson ninja

%if %{with gtkdoc}
BuildRequires:	gtk-doc
%endif
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

%if !%{with bootstrap}
%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{girname}
GObject Introspection interface description for %{name}.
%endif

%package -n %{devname}
Summary:	Libraries and include files with %{name}
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{EVRD}
%if !%{with bootstrap}
Requires:	%{girname} = %{EVRD}
%endif
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package provides the necessary development libraries and include 
files to allow you to develop with %{name}.

%prep
%autosetup -p1
%meson \

%if %{with bootstrap}	
	-Denable-introspection=no \
%endif

%if %{with gtkdoc}
	-Denable_docs=true \
%endif
	-Dsystemd_user_dir=%{_prefix}/lib/systemd/user

%build
%ninja -C build

%install
DESTDIR="%{buildroot}" %ninja install -C build

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING AUTHORS README
%{_prefix}/lib/systemd/user/at-spi-dbus-bus.service
%{_sysconfdir}/xdg/autostart/at-spi-dbus-bus.desktop
%{_libexecdir}/at-spi2-registryd
%{_libexecdir}/at-spi-bus-launcher
%{_datadir}/dbus-1/services/org.*.service
%{_datadir}/dbus-1/accessibility-services/org.*.service
%{_datadir}/defaults/at-spi2

%files -n %{libname}
%{_libdir}/libatspi.so.%{major}*

%if !%{with bootstrap}
%files -n %{girname}
%{_libdir}/girepository-1.0/Atspi-%{api}.typelib
%endif

%files -n %{devname}
%if %{with gtkdoc}
%doc %{_datadir}/gtk-doc/html/libatspi
%endif
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%if !%{with bootstrap}
%{_datadir}/gir-1.0/Atspi-%{api}.gir
%endif
