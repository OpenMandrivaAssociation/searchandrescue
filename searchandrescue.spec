%define		oname	SearchAndRescue

Name:		searchandrescue
Version:	1.4.0
Release:	%mkrel 1
Summary:	Helicopter simulator
License:	GPLv2
Group:		Games/Other
Url:		http://searchandrescue.sourceforge.net/
Source0:	http://sourceforge.net/projects/searchandrescue/files/Program/%{oname}-%{version}.tar.gz
# Make the game display correct version 1.4.0 instead of 1.3.0
Patch0:		searchandrescue-1.4.0-version.patch
Requires:	%{name}-data
Buildrequires:	jsw-devel
Buildrequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	libxpm-devel
BuildRequires:	mesagl-devel
BuildRequires:	mesaglu-devel
BuildRequires:	libxxf86vm-devel
BuildRequires:	libxxf86vm-static-devel
BuildRequires:	libsm-devel
BuildRequires:	libice-devel
BuildRequires:	libxmu-devel
Buildrequires:	imagemagick
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Changing the pace of recent sterotypical game themes, Search and Rescue aims to
create a plot based on positive goals such as saving victims in varying
situations of distress.
The player will be given the chance to pilot different types of rescue aircraft
in a variety of search and rescue style missions.
Search and Rescue is highly customizeable by allowing intermediate players to
create their own missions and allowing experianced players to design their own
aircraft and scenery.

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1 -b .ver

%build
export CFLAGS="%{optflags} -D__USE_BSD -DHAVE_SDL_MIXER -Wno-write-strings -DNEW_GRAPHICS"
export LD_LIBRARY_PATH=%{_libdir}
export CPP="g++ %{ldflags} "
./configure Linux -v --libdir="-L%{_libdir}" --disable=Y2
make all

%install
rm -rf %{buildroot}
make PREFIX=%{buildroot}%{_prefix} MAN_DIR=%{buildroot}%{_mandir}/man6 install

# icons
convert sar/icons/%{oname}.xpm -resize 16x16 %{name}-16.png
convert sar/icons/%{oname}.xpm -resize 32x32 %{name}-32.png
convert sar/icons/%{oname}.xpm %{name}-48.png
install -D -m 644 %{name}-16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 644 %{name}-32.png %{buildroot}%{_iconsdir}/%{name}.png
install -D -m 644 %{name}-48.png %{buildroot}%{_liconsdir}/%{name}.png

install -d -m 755 %{buildroot}%{_datadir}/pixmaps

mv %{buildroot}%{_gamesbindir}/%{oname} %{buildroot}%{_gamesbindir}/%{name}

# menu entry

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{oname}
Comment=%{summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;Simulation;
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS HACKING INSTALL README
%{_gamesbindir}/%{name}
%{_mandir}/man6/*
%{_datadir}/pixmaps/*.xpm
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
