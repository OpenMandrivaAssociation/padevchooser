%define name padevchooser
%define version 0.9.4
%define rel 1
%define svn 35
%if %{svn}
%define release %mkrel 0.%{svn}.%rel
%else
%define release %mkrel %rel
%endif

Summary: PulseAudio Device Chooser
Name: %{name}
Version: %{version}
Release: %{release}
%if %{svn}
Source0: %{name}-%{svn}.tar.gz
%else
Source0: %{name}-%{version}.tar.gz
%endif
# gw from debian: use stock gtk icon
Patch0: padevchooser-fix-multiple-network-ifs.patch
License: GPL
Group: Sound
Url: http://0pointer.de/lennart/projects/padevchooser/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gtk2-devel
BuildRequires: gnome-desktop-devel
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
%if %{svn}
%setup -q -n %{name}
%else
%setup -q
%endif
%patch0 -p0 -b .mutliple-net-ifs

%build
%if %{svn}
NOCONFIGURE=1 ./bootstrap.sh
%endif
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


