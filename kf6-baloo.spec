#
# Conditional build:
%bcond_with	tests		# test suite

# TODO:
# - runtime Requires if any

%define		kdeframever	6.14
%define		qtver		5.15.2
%define		kfname		baloo
Summary:	A file indexing and file search framework
Summary(pl.UTF-8):	Szkielet indeksowania i wyszukiwania plików
Name:		kf6-%{kfname}
Version:	6.14.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	9b13e46068bda372c5abc118e141316c
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	kf6-kfilemetadata-devel >= %{version}
BuildRequires:	kf6-kidletime-devel >= %{version}
BuildRequires:	kf6-kio-devel >= %{version}
BuildRequires:	lmdb-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
Conflicts:	kde4-baloo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Baloo is the file indexing and file search framework for KDE.

Baloo focuses on providing a very small memory footprint along with
with extremely fast searching. It internally uses a mixture of SQLite
along with Xapian to store the file index.

%description -l pl.UTF-8
Baloo to szkielet indeksowania i wyszukiwania plików dla KDE.

Skupia się na połączeniu bardzo małego zużycia pamięci wraz z bardzo
szybkim wyszukiwaniem. Wewnętrznie używa połączenia rozwiązań SQLite i
Xapian do przchowywania indeksu plików.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	kf6-kfilemetadata-devel >= %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%{?with_tests:%ninja_build -C build test}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kfname}6 --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}6.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/balooctl6
%attr(755,root,root) %{_bindir}/baloosearch6
%attr(755,root,root) %{_bindir}/balooshow6
%attr(755,root,root) %{_libexecdir}/kf6/baloo_file
%attr(755,root,root) %{_libexecdir}/kf6/baloo_file_extractor
%attr(755,root,root) %{_libdir}/libKF6Baloo.so.*.*.*
%ghost %{_libdir}/libKF6Baloo.so.6
%attr(755,root,root) %{_libdir}/libKF6BalooEngine.so.*.*.*
%ghost %{_libdir}/libKF6BalooEngine.so.6
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/baloosearchmodule.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/baloosearch.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/tags.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/timeline.so
%dir %{_libdir}/qt6/qml/org/kde/baloo
%{_libdir}/qt6/qml/org/kde/baloo/balooplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/baloo/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/baloo/libbalooplugin.so
%{_libdir}/qt6/qml/org/kde/baloo/qmldir
%dir %{_libdir}/qt6/qml/org/kde/baloo/experimental
%{_libdir}/qt6/qml/org/kde/baloo/experimental/baloomonitorplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/baloo/experimental/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/baloo/experimental/libbaloomonitorplugin.so
%{_libdir}/qt6/qml/org/kde/baloo/experimental/qmldir
%{_datadir}/dbus-1/interfaces/org.kde.BalooWatcherApplication.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.file.indexer.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.fileindexer.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.main.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.scheduler.xml
%{_datadir}/qlogging-categories6/baloo.categories
%{_datadir}/qlogging-categories6/baloo.renamecategories
%{systemduserunitdir}/kde-baloo.service
/etc/xdg/autostart/baloo_file.desktop

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF6Baloo.so
%{_includedir}/KF6/Baloo
%{_libdir}/cmake/KF6Baloo
%{_pkgconfigdir}/KF6Baloo.pc
