%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define major	0
%define api	2.0
%define libname	%mklibname atspi %{major}
%define girname	%mklibname atspi-gir %{api}
%define devname	%mklibname -d atspi
%bcond_with	bootstrap

Summary:	Protocol definitions and daemon for D-Bus at-spi
Name:		at-spi2-core
Version:	2.8.0
Release:	3
Epoch:		1
Group:		System/Libraries
License:	LGPLv2+
Url:		http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Source0:	http://ftp.gnome.org/pub/GNOME/sources/at-spi2-core/%{url_ver}/%{name}-%{version}.tar.xz

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

%if !%{with bootstrap}
%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.
%endif

%package -n %{devname}
Summary:	Libraries and include files with %{name}
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
%if !%{with bootstrap}
Requires:	%{girname} = %{version}-%{release}
%endif
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package provides the necessary development libraries and include 
files to allow you to develop with %{name}.

%prep
%setup -q

%build
%if %{with bootstrap}
export ac_cv_alignof_char=1
export ac_cv_alignof_dbind_pointer=4
export ac_cv_alignof_dbind_struct=1
export ac_cv_alignof_dbus_bool_t=4
export ac_cv_alignof_dbus_int16_t=2
export ac_cv_alignof_dbus_int32_t=4
export ac_cv_alignof_dbus_int64_t=4
export ac_cv_alignof_double=4
%endif
%configure2_5x \
	--disable-static \
%if %{with bootstrap}
	--enable-introspection=no
%endif

%make LIBS='-lgmodule-2.0'

%install
%makeinstall_std

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

%if !%{with bootstrap}
%files -n %{girname}
%{_libdir}/girepository-1.0/Atspi-%{api}.typelib
%endif

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/libatspi
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%if !%{with bootstrap}
%{_datadir}/gir-1.0/Atspi-%{api}.gir
%endif
