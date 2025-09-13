#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeframever	6.18
%define		kf_ver		%{version}
%define		qt_ver		6.7.0
%define		kfname		baloo
Summary:	A file indexing and file search framework
Summary(pl.UTF-8):	Szkielet indeksowania i wyszukiwania plików
Name:		kf6-%{kfname}
Version:	6.18.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	7cd2badebc8e953594e83d7be6cac570
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6DBus-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Network-devel >= %{qt_ver}
BuildRequires:	Qt6Qml-devel >= %{qt_ver}
BuildRequires:	Qt6Quick-devel >= %{qt_ver}
BuildRequires:	Qt6Test-devel >= %{qt_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf6-kconfig-devel >= %{kf_ver}
BuildRequires:	kf6-kcoreaddons-devel >= %{kf_ver}
BuildRequires:	kf6-kcrash-devel >= %{kf_ver}
BuildRequires:	kf6-kdbusaddons-devel >= %{kf_ver}
BuildRequires:	kf6-kfilemetadata-devel >= %{kf_ver}
BuildRequires:	kf6-ki18n-devel >= %{kf_ver}
BuildRequires:	kf6-kidletime-devel >= %{kf_ver}
BuildRequires:	kf6-kio-devel >= %{kf_ver}
BuildRequires:	kf6-solid-devel >= %{kf_ver}
BuildRequires:	lmdb-devel
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qt_ver}
Requires:	Qt6DBus >= %{qt_ver}
Requires:	Qt6Gui >= %{qt_ver}
Requires:	Qt6Qml >= %{qt_ver}
Requires:	kf6-dirs
Requires:	kf6-kconfig >= %{kf_ver}
Requires:	kf6-kcoreaddons >= %{kf_ver}
Requires:	kf6-kcrash >= %{kf_ver}
Requires:	kf6-kdbusaddons >= %{kf_ver}
Requires:	kf6-kfilemetadata >= %{kf_ver}
Requires:	kf6-ki18n >= %{kf_ver}
Requires:	kf6-kidletime >= %{kf_ver}
Requires:	kf6-kio >= %{kf_ver}
Requires:	kf6-solid >= %{kf_ver}
Provides:	kf5-baloo-service = %{version}-%{release}
Obsoletes:	kf5-baloo-service < 6
Conflicts:	kde4-baloo
Conflicts:	kf5-baloo < 5.116.0-2
%requires_eq_to Qt6Core Qt6Core-devel
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
Requires:	Qt6Core-devel >= %{qt_ver}
Requires:	kf6-kcoreaddons-devel >= %{kf_ver}
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

%find_lang %{kfname}6 --all-name

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
