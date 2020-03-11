Name:           ecf-global
Group:          System Environment/Libraries
Version:        1.0.16
Release:        0%{?dist}
Summary:        ECF Global RPM
URL:            https://github.com/tskirvin/ecf-global

License:        Artistic 2.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  rsync perl-podlators
%if 0%{?rhel} == 6
Requires:       python-simplejson shyaml
%endif

%if 0%{?rhel} == 7
Requires:       python-simplejson shyaml
%endif

%if 0%{?rhel} == 8
Requires:       python2-simplejson shyaml
%endif

Source:         ecf-global-%{version}-%{release}.tar.gz

%description
Globally installed scripts and tools for ECF systems at Fermi Lab.

%prep
%setup -c -n ecf-global -q

%build
# Empty build section added per rpmlint

%install
rm -rf $RPM_BUILD_ROOT

rsync -Crlpt ./etc ${RPM_BUILD_ROOT}
rsync -Crlpt ./opt ${RPM_BUILD_ROOT}
rsync -Crlpt ./usr ${RPM_BUILD_ROOT}
rsync -Crlpt ./var ${RPM_BUILD_ROOT}

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

%post

%clean
# Adding empty clean section per rpmlint.  In this particular case, there is
# nothing to clean up as there is no build process

%files
%attr(-, root, root) %{_sbindir}/*
%attr(-, root, root) %{_mandir}/*/*
%attr(-, root, root) %{_libexecdir}/ecf-global/*
%attr(-, root, root) %config(noreplace) /etc/ecf-global/*
%attr(-, root, root) /etc/cron.d/*
%attr(-, root, root) /var/cache/ecf-global/.placeholder
%attr(-, root, root) /opt/ssi/check_mk_agent/lib/local/ssi_yumcache_*

%changelog
* Wed Mar 11 2020   Tim Skirvin <tskirvin@fnal.gov> 1.0.16-0
- ssi_check_yumcache_to_patch - removind underscores to make check_mk happy

* Tue Dec  3 2019   Tim Skirvin <tskirvin@fnal.gov> 1.0.15-0
- adding CentOS 8 support (mostly .spec file changes)t diff
- yumcache-build-from-cache - now invokes python2

* Wed Sep 25 2019   Tim Skirvin <tskirvin@fnal.gov> 1.0.14-0
- yumcache-build-from-cache - removing python2.6 reference, python
  formatting tweaks to match the linter
- /usr/sbin/puppet-templock - invokes the two libexec yumcache scripts

* Tue Jun 18 2019   Tim Skirvin <tskirvin@fnal.gov> 1.0.13-1
- puppet-templock - typo bug fixes

* Tue Jun 18 2019   Tim Skirvin <tskirvin@fnal.gov> 1.0.13-0
- puppet-templock - lock puppet with a reason, unlock with at in 24 hours

* Wed Oct 03 2018   Tim Skirvin <tskirvin@fnal.gov> 1.0.12-0
- puppet-dryrun - adding '--trace' option (no actual release)

* Fri Aug 24 2018   Tim Skirvin <tskirvin@fnal.gov> 1.0.11-0
- yumcache-cache - actually listening to the config file timeout; making
  this configurable at the command line

* Thu Mar 29 2018   Tim Skirvin <tskirvin@fnal.gov> 1.0.10-1
- ssi_yumcache_security_to_patch - don't skip openafs anymore

* Thu Jan 25 2018   Tim Skirvin <tskirvin@fnal.gov> 1.0.10-0
- ssi_yumcache_security_to_patch - report package counts for graphing

* Mon Oct 30 2017   Tim Skirvin <tskirvin@fnal.gov>  1.0.9-0
- /etc/cron.d/slf-repo-kill - remove /etc/yumrepos.d/slf.repo via cron

* Tue Sep 19 2017   Tim Skirvin <tskirvin@fnal.gov>  1.0.8-0
- added a '--force' flag to puppet-dryrun
- dropping SL5 support

* Mon Mar 27 2017   Tim Skirvin <tskirvin@fnal.gov>  1.0.7-0
- change the error codes for ssi_yumcache_security_to_patch 

* Thu Mar 16 2017   Tim Skirvin <tskirvin@fnal.gov>  1.0.6-0
- fef_kernel_expired -> ssi_kernel_expired

* Mon May 23 2016   Tim Skirvin <tskirvin@fnal.gov>  1.0.5-0
- ssi_yumcache_security_to_patch - also filter afs/kmod lines
- yumcache-build-from-cache - use env to find python2.6

* Wed Apr 20 2016  Tim Skirvin <tskirvin@fnal.gov>  1.0.4-4
- yumcache-build-from-cache - python2.6 runs with usr/bin/env

* Wed Mar 23 2016  Tim Skirvin <tskirvin@fnal.gov>  1.0.4-3
- work on the yumcache-cache cron jobs
- removing the post script
- yumcache-cache is no longer silent

* Wed Mar 23 2016  Tim Skirvin <tskirvin@fnal.gov>  1.0.4-2
- cron jobs don't send email anymore
- .spec file fixes

* Fri Mar 18 2016  Tim Skirvin <tskirvin@fnal.gov>  1.0.4-1
- using python2.6 so that RHEL5 can use its yaml

* Fri Mar 18 2016  Tim Skirvin <tskirvin@fnal.gov>  1.0.4-0
- added 'yumcache' suite
- 'timeout3' script into /usr/libexec for convenience
- post-install script

* Mon Mar 14 2016  Tim Skirvin <tskirvin@fnal.gov>  1.0.3-0
- puppet-dryrun - added 'tags'

* Fri Feb  5 2016  Tim Skirvin <tskirvin@fnal.gov>  1.0.2-0
- giving up on python-compat

* Fri Feb  5 2016  Tim Skirvin <tskirvin@fnal.gov>  1.0.1-0
- renamed puppet-test to puppet-dryrun
- moved iptables-report to /usr/libexec

* Thu Feb  4 2016  Tim Skirvin <tskirvin@fnal.gov>  1.0.0-0
- initial version
