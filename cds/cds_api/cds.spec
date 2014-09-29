Name:           pulp-v2-cds-server
Version:        1.0.2
Release:        1%{?dist}
Summary:        Server plugin for pulp v2 server to distribute content.

Group:          Development/Languages
License:        GPLv2
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  rpm-python

Requires: mod_wsgi
Requires: mod_ssl
Conflicts: pulp-v2-cds

%description
Server plugin for pulp v2 server to distribute content.

%prep
%setup -q 

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
cp etc/httpd/conf.d/cds_api.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/

mkdir -p $RPM_BUILD_ROOT/etc/rhui
cp -r etc/rhui/* $RPM_BUILD_ROOT/etc/rhui/

mkdir -p $RPM_BUILD_ROOT/srv/pulp/
cp srv/pulp/* $RPM_BUILD_ROOT/srv/pulp

mkdir -p $RPM_BUILD_ROOT/%{python_sitelib}/pulp/cds/
cp -r src/* $RPM_BUILD_ROOT/%{python_sitelib}/pulp/cds/

mkdir -p $RPM_BUILD_ROOT/var/log/pulp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,apache,apache,-)
%{python_sitelib}/pulp/cds/
%attr(775, apache, apache) /srv/pulp
%config %{_sysconfdir}/httpd/conf.d/cds_api.conf
%config %{_sysconfdir}/rhui/rhui_cds.conf
%config %{_sysconfdir}/rhui/cds/logging.cfg
%attr(3775, apache, apache) /var/log/pulp

%post
semanage fcontext -a -t httpd_user_rw_content_t '/srv/pulp(/.*)?'
restorecon -Rv /srv/pulp/*

%postun
if [ $1 -eq 0] ; then # final removal
semanage fcontext -d -t httpd_user_rw_content_t '/srv/pulp(/.*)?'
fi

%changelog
* Mon Sep 29 2014 David Gao <jinmaster923@gmail.com> 1.0.2-1
- Updated unit tests. (jinmaster923@gmail.com)
- Renamed folders from cds to pulp_cds. (jinmaster923@gmail.com)
- Updated model: 'cdses' is ['string'] (jinmaster923@gmail.com)
- Added cluster info and update functionality. (jinmaster923@gmail.com)
- Initial cds cluster list/create work. (jinmaster923@gmail.com)
- Changed CDS model to have sync_schedule instead of update_time. Included
  cluster_id to model (jinmaster923@gmail.com)
- Fix: "sslv3 alert unexpected message"  Change wsgi config from:
  SSLVerifyClient none to "SSLVerifyClient optional"  Prior to this on server
  we saw messages like:  (103)Software caused connection abort: mod_wsgi
  (pid=9429): Unable to get bucket brigade for request. (jwmatthews@gmail.com)
- Updated python module for CDS from pulp.cds to pulp_cds.cds   Avoids conflict
  with pulp's own module (jwmatthews@gmail.com)
- Change import path from rhui_cds to pulp.cds (jinmaster923@gmail.com)
- Moved installed source files from /usr/lib/python_2.x/site-packages/pulp to
  /usr/lib/python_2.x/site-packages/pulp/cds/. (jinmaster923@gmail.com)
- Added rhui/*.cfg to %%file section. (jinmaster923@gmail.com)

* Thu Aug 07 2014 David Gao <jinmaster923@gmail.com> 1.0.1-1
- new package built with tito

