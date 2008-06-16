%define name    searchandrescue
%define Name    SearchAndRescue
%define version 0.8.2
%define release %mkrel 6

%define title       SearchAndRescue
%define longtitle   Helicopter simulator

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Helicopter simulator
License:        GPL
Group:          Games/Other
Url:            http://wolfpack.twu.net/SearchAndRescue/index.html
Source0:        http://wolfpack.twu.net/users/wolfpack/%{Name}-%{version}.tar.bz2
Patch0:         %{name}-0.8.2.gcc4.patch
Requires:       %{name}-data
Buildrequires:  libjsw-devel
Buildrequires:  libyiff-devel
Buildrequires:  X11-devel
Buildrequires:  Mesa-common-devel
Buildrequires:  ImageMagick
BuildRoot:      %{_tmppath}/%{name}-%{version}

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
%setup -q -n %{Name}-%{version}
%patch0 -p1

%build
export CFLAGS="%{optflags}"
export LD_LIBRARY_PATH=%{_libdir}:%{_prefix}/X11R6/%{_lib}
./configure Linux -v --disable=arch-i686 --libdir="-L%{_libdir} -L%{_prefix}/X11R6/%{_lib}"
%make all

%install
rm -rf %{buildroot}
make PREFIX=%{buildroot}%{_prefix} MAN_DIR=%{buildroot}%{_mandir}/man6 install

# icons
convert sar/icons/%{Name}.xpm -resize 16x16 %{name}-16.png
convert sar/icons/%{Name}.xpm -resize 32x32 %{name}-32.png
convert sar/icons/%{Name}.xpm %{name}-48.png
install -D -m 644 %{name}-16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 644 %{name}-32.png %{buildroot}%{_iconsdir}/%{name}.png 
install -D -m 644 %{name}-48.png %{buildroot}%{_liconsdir}/%{name}.png 

# menu entry

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{longtitle}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game/Simulation;
EOF

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files
%defattr(-,root,root)
%doc AUTHORS  HACKING  INSTALL  LICENSE  README
%{_gamesbindir}/*
%{_mandir}/man6/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{Name}*.xpm
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


