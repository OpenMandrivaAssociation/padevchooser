%define name padevchooser
%define version 0.9.3
%define release %mkrel 3

Summary: PulseAudio Device Chooser
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
# gw from debian: use stock gtk icon
Patch0: padevchooser-0.9.3-use_stock_g2.14_icons.dpatch
Patch1: padevchooser-fix-multiple-network-ifs.patch
License: GPL
Group: Sound
Url: http://0pointer.de/lennart/projects/padevchooser/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gtk2-devel
BuildRequires: libglade2.0-devel
BuildRequires: libGConf2-devel
BuildRequires: libpulseaudio-devel >= 0.9.5
BuildRequires: libnotify-devel
BuildRequires: lynx
BuildRequires: desktop-file-utils
Requires: pulseaudio
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
PulseAudio Device Chooser is a simple GTK tool which registers an icon
in the tray area and allows quick access to some features of the
PulseAudio sound server. Specifically it can do for you:

* Notify about new sink/sources becoming available on the LAN
* Quickly change the default PulseAudio sink/source/server assigned to
  the current X11 display, selecting devices available on the LAN
* Start the auxiliary tools PulseAudio Volume Control, PulseAudio
  Volume Meter, PulseAudio Manager, PulseAudio Preferences

%prep
%setup -q
%patch0 -p1 -b .stock-icons
%patch1 -p0 -b .mutliple-net-ifs

%build
#export CPPFLAGS=-I%_includedir/alsa
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --add-category="X-MandrivaLinux-Multimedia-Sound" \
  --remove-category="Application" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%post
%update_desktop_database

%postun
%clean_desktop_database

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README LICENSE
%_bindir/%name
%_datadir/applications/%name.desktop
%_datadir/%name/%name.glade


