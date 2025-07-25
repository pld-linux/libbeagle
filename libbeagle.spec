#
# Conditional build:
%bcond_with	apidocs		# build API documentation
%bcond_without	python		# don't build python libraries

Summary:	Beagle C interface
Summary(pl.UTF-8):	Interfejs w C do Beagle
Name:		libbeagle
Version:	0.3.9
Release:	9
License:	MIT
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libbeagle/0.3/%{name}-%{version}.tar.bz2
# Source0-md5:	af1e25bdfb704ee87047bc49a73fbb10
Patch0:		%{name}-am.patch
Patch1:		format-security.patch
Patch2:		build.patch
URL:		http://beagle-project.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-dtd412-xml
BuildRequires:	glib2-devel >= 1:2.6.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.0}
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.19
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-pygobject-devel >= 2.6.0
BuildRequires:	python-pygtk-devel >= 2:2.6.0
BuildRequires:	rpm-pythonprov
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Beagle C interface.

%description -l pl.UTF-8
Interfejs w C do Beagle.

%package devel
Summary:	Header files for libbeagle library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbeagle
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.6.0
Requires:	libxml2-devel >= 1:2.6.19

%description devel
Header files for libbeagle library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbeagle.

%package static
Summary:	Static libbeagle library
Summary(pl.UTF-8):	Statyczna biblioteka libbeagle
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbeagle library.

%description static -l pl.UTF-8
Statyczna biblioteka libbeagle.

%package apidocs
Summary:	libbeagle API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libbeagle
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
libbeagle API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libbeagle.

%package examples
Summary:	libbeagle - example programs
Summary(pl.UTF-8):	libbeagle - przykładowe programy
Group:		Libraries
BuildArch:	noarch

%description examples
libbeagle - example programs.

%description examples -l pl.UTF-8
libbeagle - przykładowe programy.

%package -n python-beagle
Summary:	Beagle Python bindings
Summary(pl.UTF-8):	Wiązania języka Python dla Beagle
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs

%description -n python-beagle
Beagle Python bindings.

%description -n python-beagle -l pl.UTF-8
Wiązania języka Python dla Beagle.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PYTHON=%{__python} \
	%{?with_apidocs:--enable-gtk-doc} \
	--with-html-dir=%{_gtkdocdir}

%{__make} \
	pythondir=%{py_sitedir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pythondir=%{py_sitedir}

cp examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%if %{with python}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/beagle/beagle.{a,la}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libbeagle.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbeagle.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbeagle.so
%{_libdir}/libbeagle.la
%{_includedir}/libbeagle
%{_pkgconfigdir}/libbeagle-1.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libbeagle.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/beagle
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/libbeagle-%{version}

%if %{with python}
%files -n python-beagle
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/beagle/beagle.so
%dir %{py_sitedir}/beagle
%{py_sitedir}/beagle/*.py[co]
%endif
