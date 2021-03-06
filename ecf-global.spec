Name:           ecf-global
Group:          System Environment/Libraries
Version:        1.0.1
Release:        0%{?dist}
Summary:        ECF Global RPM
URL:            https://github.com/tskirvin/ecf-global

License:        Fermitools Software Legal Information (Modified BSD License)
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rsync
Requires:       python-simplejson

Source:         ecf-global-%{version}-%{release}.tar.gz

%description
Globally installed scripts and tools for ECF systems at Fermi Lab.

%prep
%setup -c -n ecf-global -q

%build
# Empty build section added per rpmlint

%install
rm -rf $RPM_BUILD_ROOT

rsync -Crlpt ./usr ${RPM_BUILD_ROOT}

if [ -d usr/sbin ]; then
    mkdir -p ${RPM_BUILD_ROOT}/usr/share/man/man8
    for i in `ls usr/sbin`; do
        pod2man --section 8 --center="System Commands" usr/sbin/${i} \
            > ${RPM_BUILD_ROOT}/usr/share/man/man8/${i}.8 ;

    done
fi

if [ -d usr/bin ]; then
    mkdir -p ${RPM_BUILD_ROOT}/usr/share/man/man1
    for i in `ls usr/bin`; do
        pod2man --section 1 --center="System Commands" usr/bin/${i} \
            > ${RPM_BUILD_ROOT}/usr/share/man/man1/${i}.1 ;
    done
fi

%clean
# Adding empty clean section per rpmlint.  In this particular case, there is 
# nothing to clean up as there is no build process

%files
%attr(-, root, root) %{_bindir}/*
%attr(-, root, root) %{_sbindir}/*
%attr(-, root, root) %{_mandir}/*/*
%attr(-, root, root) %{_libexecdir}/ecf-global/*

%changelog
* Fri Feb  5 2016  Tim Skirvin <tskirvin@fnal.gov>  1.0.1-0
- renamed puppet-test to puppet-dryrun
- moved iptables-report to /usr/libexec

* Thu Feb  4 2016  Tim Skirvin <tskirvin@fnal.gov>  1.0.0-0
- initial version
