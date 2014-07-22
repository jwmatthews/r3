Name:           pulp-v2-cds
Version:        1.0.2
Release:        1%{?dist}
Summary:        A lightweight distribution system for pulp v2 content. 

Group:          Development/Languages
License:        GPLv2
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  rpm-python

Requires: mod_wsgi
Requires: mod_ssl

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

mkdir -p $RPM_BUILD_ROOT/etc/pki/pulp
cp -r etc/pki/pulp/* .

mkdir -p $RPM_BUILD_ROOT/var/lib/pulp-cds
mkdir -p $RPM_BUILD_ROOT/var/log/pulp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,apache,apache,-)
%{python_sitelib}/pulp/cds/
%attr(775, apache, apache) %{_sysconfdir}/pki/pulp/
%attr(775, apache, apache) %{_sysconfdir}/pki/pulp/content
%attr(775, apache, apache) /srv/pulp
%attr(750, apache, apache) /srv/pulp/cds_api.wsgi
%attr(750, apache, apache) /srv/pulp/lb.wsgi
%attr(750, apache, apache) /srv/pulp/repo_auth.wsgi
%config %{_sysconfdir}/httpd/conf.d/pulp-cds.conf
%config(noreplace) %{_sysconfdir}/pulp/repo_auth.conf
%attr(3775, root, root) %{_sysconfdir}/pki/pulp/content
%attr(3775, apache, apache) /var/lib/pulp-cds
%attr(3775, apache, apache) /var/log/pulp

# EDIT SELINUX CONTEXT FOR WSGI

%changelog
* Tue Jul 22 2014 David Gao <jinmaster923@gmail.com> 1.0.2-1
- Bumping version to 1.0.1 (jinmaster923@gmail.com)
- Initial update for producing rsync list based on repo ids provided.
  (jinmaster923@gmail.com)
- Adding test code for generating a list of files to rsync
  (jwmatthews@gmail.com)
- Moved cds unit tests to unit dir, so we may introduce integration tests
  (jwmatthews@gmail.com)
- Restructing unit tests for CDS (jwmatthews@gmail.com)
- Created /etc/pki/pulp/content folder (jinmaster923@gmail.com)
- Update to the latest version of repo_auth.wsgi (jinmaster923@gmail.com)
- Corrected some python errors (jinmaster923@gmail.com)
- Corrected new import path (jinmaster923@gmail.com)
- Initial modifications for permission issues. (jinmaster923@gmail.com)
- Added lb.wsgi Added NullHandler to handle situations where apache does not
  have logging handler. (jinmaster923@gmail.com)
- Re-add lb content back to conf file (jinmaster923@gmail.com)
- Correct typo (jinmaster923@gmail.com)
- Removed cds api section in pulp-cds.conf Added paths needed to be used for
  CDS (jinmaster923@gmail.com)
- Oops, correct cp path mistake from last commit (jinmaster923@gmail.com)
- Added python src files. (jinmaster923@gmail.com)
- Automatic commit of package [pulp-v2-cds] release [1.0.1-1].
  (jinmaster923@gmail.com)
- Initial commit for cds rpm work. (jinmaster923@gmail.com)
- Initialized to use tito. (jinmaster923@gmail.com)

* Tue Jul 22 2014 David Gao <jinmaster923@gmail.com>
- Initial update for producing rsync list based on repo ids provided.
  (jinmaster923@gmail.com)
- Adding test code for generating a list of files to rsync
  (jwmatthews@gmail.com)
- Moved cds unit tests to unit dir, so we may introduce integration tests
  (jwmatthews@gmail.com)
- Restructing unit tests for CDS (jwmatthews@gmail.com)
- Created /etc/pki/pulp/content folder (jinmaster923@gmail.com)
- Update to the latest version of repo_auth.wsgi (jinmaster923@gmail.com)
- Corrected some python errors (jinmaster923@gmail.com)
- Corrected new import path (jinmaster923@gmail.com)
- Initial modifications for permission issues. (jinmaster923@gmail.com)
- Added lb.wsgi Added NullHandler to handle situations where apache does not
  have logging handler. (jinmaster923@gmail.com)
- Re-add lb content back to conf file (jinmaster923@gmail.com)
- Correct typo (jinmaster923@gmail.com)
- Removed cds api section in pulp-cds.conf Added paths needed to be used for
  CDS (jinmaster923@gmail.com)
- Oops, correct cp path mistake from last commit (jinmaster923@gmail.com)
- Added python src files. (jinmaster923@gmail.com)
- Automatic commit of package [pulp-v2-cds] release [1.0.1-1].
  (jinmaster923@gmail.com)
- Initial commit for cds rpm work. (jinmaster923@gmail.com)
- Initialized to use tito. (jinmaster923@gmail.com)
