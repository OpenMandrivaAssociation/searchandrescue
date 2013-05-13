%define Name    SearchAndRescue

%define title       SearchAndRescue
%define longtitle   Helicopter simulator

Name:           searchandrescue
Version:        1.4.0
Release:        2
Summary:        Helicopter simulator
License:        GPL
Group:          Games/Other
Url:            http://searchandrescue.sourceforge.net/
Source0:        http://switch.dl.sourceforge.net/project/searchandrescue/Program/SearchAndRescue-%version.tar.gz
Patch0:		SearchAndRescue-1.1.0-link.patch
Patch1:		searchandrescue-1.4.0-compile.patch
Requires:       %{name}-data
Buildrequires:  jsw-devel
Buildrequires:  yiff-devel
Buildrequires:  SDL-devel
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	mesagl-devel
BuildRequires:	mesaglu-devel
BuildRequires:	pkgconfig(xxf86vm)
Buildrequires:  imagemagick

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
%patch0 -p0 -b .link~
%patch1 -p1 -b .compile~

%build
export CFLAGS="%{optflags}"
export LD_LIBRARY_PATH=%{_libdir}
export CPP="g++ %ldflags "
./configure Linux -v --disable=arch-i686 --libdir="-L%{_libdir}"
make all

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

install -d -m 755 %{buildroot}%{_datadir}/pixmaps

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
Categories=Game;Simulation;
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
%doc AUTHORS  HACKING  INSTALL  README
%{_gamesbindir}/*
%{_mandir}/man6/*
%{_datadir}/pixmaps/*.xpm
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


%changelog
* Sun Mar 13 2011 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.0-1mdv2011.0
+ Revision: 644439
- new version

* Thu Feb 10 2011 Funda Wang <fwang@mandriva.org> 1.1.0-2
+ Revision: 637138
- more linakge fix
- tighten BR

* Sat Nov 13 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.0-1mdv2011.0
+ Revision: 597288
- new version

* Fri Jul 16 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.0-1mdv2011.0
+ Revision: 554132
- update to new version 1.0.0

* Sun Mar 21 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.8.4-1mdv2010.1
+ Revision: 526017
- update to new version 0.8.4

* Sun Mar 14 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.8.3-1mdv2010.1
+ Revision: 519098
- fix build dependencies
- new version
- drop old patches
- new URL

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sun Jan 25 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.8.2-6mdv2009.1
+ Revision: 333566
- ditch 'LICENSE' file since we already carry copyleft notice for GPL in
  the common-licenses package
- fix build (P1)

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - fix description-line-too-long
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel
    - kill desktop-file-validate's error: string list key "Categories" in group "Desktop Entry" does not have a semicolon (";") as trailing character
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Wed Feb 14 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.8.2-5mdv2007.0
+ Revision: 121010
- rebuild against current libjsw

* Wed Aug 02 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.8.2-4mdv2007.0
- xdg menu 
- rediff patch 0

* Mon Dec 12 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.8.2-3mdk
- Fixes from Anssi Hannula (<anssi.hannula@gmail.com>): 
 - fix libdirs for lib64
 - fix menudir
- Drop obsoletes

* Thu Aug 18 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.8.2-2mdk
- fixed build with gcc 4
- renamed to searchandrescue
- %%mkrel
- spec cleanup
- split data in a distinct subpackage

* Tue Sep 07 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.8.2-1mdk
- 0.8.2

* Fri Aug 27 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.8.1-4mdk
- rebuild for new menu
- cosmetics

* Fri Jul 23 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.8.1-3mdk 
- explicit --libdir

* Sun Jun 06 2004 Guillaume Rousse <guillomovitch@mandrake.org> 0.8.1-2mdk
- rebuild
- rpmbuilupdate aware
- no more explicit requires
- fixed buildrequires
- fixed menu section

