Name:       time
Summary:    A GNU utility for monitoring a program's use of system resources
Version:    1.7
Release:    34
Group:      Applications/System
License:    GPLv2+
URL:        http://www.gnu.org/software/time/
Source0:    ftp://prep.ai.mit.edu/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Patch0:     time-1.7-destdir.patch
Patch1:     time-1.7-verbose.patch
Patch2:     fix-info-direntry.patch
BuildRequires:  texinfo

%description
The GNU time utility runs another program, collects information about
the resources used by that program while it is running, and displays
the results.

%package doc
Summary:    Documentation files for %{name}
Group:      Documentation
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info
Obsoletes:  %{name}-docs

%description doc
Info pages for %{name}.

%prep
%setup -q -n %{name}-%{version}

# time-1.7-destdir.patch
%patch0 -p1
# time-1.7-verbose.patch
%patch1 -p1
# fix-info-direntry.patch
%patch2 -p1

%build
echo "ac_cv_func_wait3=\${ac_cv_func_wait3='yes'}" >> config.cache

%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/%{_docdir}/%{name}-%{version}
install -m0644 -t %{buildroot}/%{_docdir}/%{name}-%{version} \
        NEWS README

%post doc
%install_info --info-dir=%_infodir %{_infodir}/time.info.gz

%postun doc
if [ $1 = 0 ] ;then
%install_info_delete --info-dir=%{_infodir} %{_infodir}/time.info.gz
fi

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/time

%files doc
%defattr(-,root,root,-)
%{_infodir}/time.info.gz
%{_docdir}/%{name}-%{version}
