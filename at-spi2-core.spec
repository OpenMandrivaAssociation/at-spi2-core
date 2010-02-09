Name:           at-spi2-core
Version:        0.1.6
Release:        %mkrel 1
Summary:        Protocol definitions and daemon for D-Bus at-spi

Group:          System/Libraries
License:        LGPLv2+
URL:            http://www.linuxfoundation.org/en/AT-SPI_on_D-Bus
Source0:        http://download.gnome.org/sources/at-spi2-core/0.1/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk2-devel
BuildRequires:  libxtst-devel

Requires:       dbus

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.


%prep
%setup -q

%build
%configure2_5x
%make


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS README
%{_libexecdir}/at-spi2-registryd
%{_datadir}/at-spi2
%{_datadir}/dbus-1/services/org.freedesktop.atspi.Registry.service

