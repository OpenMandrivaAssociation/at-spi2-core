%define major		0
%define gir_major	2.0
%define libname		%mklibname atspi %{major}
%define girname		%mklibname atspi-gir %{gir_major}
%define develname 	%mklibname -d atspi

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Name:		at-spi2-core
Version:	2.5.1
Release:	1
Summary:	Protocol definitions and daemon for D-Bus at-spi
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

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
%dir %_sysconfdir/at-spi2/
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

