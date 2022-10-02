# at-spi2-core is used by at-spi2-atk, at-spi2-atk is used by gtk-3.0,
# gtk-3.0 is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define major	0
%define api	2.0
%define libname	%mklibname atspi %{major}
%define girname	%mklibname atspi-gir %{api}
%define devname	%mklibname -d atspi
%define lib32name	%mklib32name atspi %{major}
%define dev32name	%mklib32name -d atspi
%bcond_with	bootstrap
%bcond_with	gtkdoc

Summary:	Protocol definitions and daemon for D-Bus at-spi
Name:		at-spi2-core
Version:	2.46.0
Release:	1
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
BuildRequires:	pkgconfig(libpcre2-8)
BuildRequires:	pkgconfig(libxml-2.0)
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

%if %{with compat32}
BuildRequires:	devel(libdbus-1)
BuildRequires:	devel(libgio-2.0)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libgobject-2.0)
BuildRequires:	devel(libpcre2-8)
BuildRequires:	devel(libxml-2.0)
BuildRequires:	devel(libz)
BuildRequires:	devel(libbz2)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXi)
BuildRequires:	devel(libXtst)
BuildRequires:	devel(libsystemd)
BuildRequires:	devel(libxkbcommon)
%endif

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

%if %{with compat32}
%package -n %{lib32name}
Summary:	Libraries for %{name} (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains libraries used by %{name}.

%package -n %{dev32name}
Summary:	Libraries and include files with %{name} (32-bit)
Group:		Development/GNOME and GTK+
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}

%description -n %{dev32name}
This package provides the necessary development libraries and include 
files to allow you to develop with %{name}.
%endif

%prep
%autosetup -p1
%if %{with compat32}
%meson32 \
	-Dintrospection=no \
	-Ddocs=false \
	-Dx11=yes \
	-Dsystemd_user_dir=%{_prefix}/lib/systemd/user \
	-Ddbus_daemon=/usr/bin/dbus-daemon
%endif

%meson \
%if %{with bootstrap}	
	-Dintrospection=no \
%endif
%if %{with gtkdoc}
	-Ddocs=true \
%endif
	-Dintrospection=yes \
	-Dx11=yes \
	-Dsystemd_user_dir=%{_prefix}/lib/systemd/user \
	-Ddbus_daemon=/usr/bin/dbus-daemon
	
# force use x11 even on compat32 because without it compilation failing with  error: use of undeclared identifier 'LockMask' if (modifiers & LockMask)
# https://gitlab.gnome.org/GNOME/at-spi2-core/-/issues/51

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%ninja -C build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
DESTDIR="%{buildroot}" %ninja install -C build

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING AUTHORS README.md
%{_prefix}/lib/systemd/user/at-spi-dbus-bus.service
%{_sysconfdir}/xdg/autostart/at-spi-dbus-bus.desktop
%{_sysconfdir}/xdg/Xwayland-session.d/00-at-spi
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

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libatspi.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
