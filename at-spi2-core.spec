Name:           at-spi2-core
Version:        2.0.1
Release:        %mkrel 1
Summary:        Protocol definitions and daemon for D-Bus at-spi
Group:          System/Libraries
License:        LGPLv2+
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Source0:        http://ftp.gnome.org/pub/GNOME/sources/%name/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  dbus-devel
BuildRequires:  glib2-devel
BuildRequires:	libx11-devel
BuildRequires:	libxtst-devel
BuildRequires:	libxevie-devel
BuildRequires:	intltool
BuildRequires:	gobject-introspection-devel
Requires:       dbus

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

%define major 0
%define libname %mklibname atspi %major

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Requires:	%name = %version

%description -n %{libname}
This package contains libraries used by %{name}.

%define libnamedev %mklibname -d atspi
%package -n %{libnamedev}
Summary:	Libraries and include files with %{name}
Group:		Development/GNOME and GTK+
Requires:	%name = %{version}
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libnamedev}
This package provides the necessary development libraries and include 
files to allow you to develop with %{name}.

%prep
%setup -q

%build
%configure2_5x --disable-static
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS README
%dir %_sysconfdir/at-spi2/
%config(noreplace) %_sysconfdir/at-spi2/accessibility.conf
%_sysconfdir/xdg/autostart/at-spi-dbus-bus.desktop
%{_libexecdir}/at-spi2-registryd
%{_libexecdir}/at-spi-bus-launcher
%{_datadir}/dbus-1/services/org.*.service

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{major}.*
%{_libdir}/girepository-1.0/Atspi-2.0.typelib

%files -n %libnamedev
%defattr(-,root,root,-)
%_libdir/*.so
%_libdir/*.la
%_libdir/pkgconfig/*.pc
%_includedir/*
%_datadir/gir-1.0/Atspi-2.0.gir
%_datadir/gtk-doc/html/libatspi
