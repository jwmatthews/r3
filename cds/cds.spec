Name:           pulp-v2-cds
Version:        1.0.0
Release:        1%{?dist}
Summary:        A lightweight distribution system for pulp v2 content. 

Group:          Development/Languages
License:        GPLv2
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  rpm-python

Requires: mod_wsgi

%description
A lightweight distribution system for pulp v2 content.

%prep
%setup -q 

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
cp etc/httpd/conf.d/pulp-cds.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/

mkdir -p $RPM_BUILD_ROOT/etc/pulp
cp etc/pulp/repo_auth.conf $RPM_BUILD_ROOT/etc/pulp/

mkdir -p $RPM_BUILD_ROOT/srv/pulp/
cp srv/pulp/* $RPM_BUILD_ROOT/srv/pulp

mkdir -p $RPM_BUILD_ROOT/%{python_sitelib}/pulp/cds/
cp -r src/* $RPM_BUILD_ROOT/%{python_sitelib}/pulp/cds/

mkdir -p $RPM_BUILD_ROOT/etc/pki/pulp/content
mkdir -p $RPM_BUILD_ROOT/var/lib/pulp-cds
mkdir -p $RPM_BUILD_ROOT/var/log/pulp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,apache,apache,-)
%{python_sitelib}/pulp/cds/
%attr(775, apache, apache) /srv/pulp
%attr(750, apache, apache) /srv/pulp/repo_auth.wsgi
%config %{_sysconfdir}/httpd/conf.d/pulp-cds.conf
%config(noreplace) %{_sysconfdir}/pulp/repo_auth.conf
%attr(3775, root, root) %{_sysconfdir}/pki/pulp/content
%attr(3775, apache, apache) /var/lib/pulp-cds
%attr(3775, apache, apache) /var/log/pulp-cds
