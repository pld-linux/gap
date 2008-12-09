Summary:	Groups, Algorithms and Programming
Summary(pl.UTF-8):	Grupy, Algorytmy i Programowanie
Name:		gap
Version:	4.4.10
Release:	1
License:	distributable
Group:		Applications/Math
Source0:	ftp://ftp.gap-system.org/pub/gap/gap4/tar.bz2/%{name}4r4p10.tar.bz2
# Source0-md5:	8b7d5fbe420cc5d8fc59c187374bc4f4
Source1:	%{name}.desktop
Patch0:		%{name}-gac.patch
URL:		http://www.gap-system.org/
BuildRequires:	ghostscript
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GAP is a free, open and extensible software package for computation in
discrete abstract algebra.

%description -l pl.UTF-8
GAP jest darmowym, otwartym i rozszerzalnym pakietem oprogramowania do
obliczeń dyskretnej abstrakcyjnej algebry.

%prep
%setup -q -c
%patch0 -p1

%build
cd gap4r4
sed -i -e 's/GP_CFLAGS//g' cnf/configure.in
%{__make} -C cnf configure.out
%configure

mkdir -p bin/%{_target_platform}
cp -f cnf/configure.out bin/%{_target_platform}/configure
cd bin/%{_target_platform}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/gap,%{_desktopdir}}

cd gap4r4

cp -a sysinfo.gap grp lib pkg prim small src trans tst $RPM_BUILD_ROOT%{_datadir}/gap/

install bin/%{_target_platform}/gap $RPM_BUILD_ROOT%{_bindir}/%{_target_platform}-gap
sed -e 's|^gap_bin=.*|gap_bin=|' bin/%{_target_platform}/gac > \
		$RPM_BUILD_ROOT%{_bindir}/gac

cat <<EOF > $RPM_BUILD_ROOT%{_bindir}/gap
#!/bin/sh
[ -z "\$GAP_MEM" ] && GAP_MEM=32m
exec %{_bindir}/%{_target_platform}-gap -m \$GAP_MEM -l %{_datadir}/gap \$*
EOF

cd doc
dvipdf new/manual.dvi new.pdf
dvipdf ext/manual.pdf extending.pdf
dvipdf prg/manual.pdf programming.pdf
dvipdf ref/manual.pdf refman.pdf
dvipdf tut/manual.pdf tutorial.pdf

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc gap4r4/doc/*.pdf gap4r4/doc/htm
%attr(755,root,root) %{_bindir}/*
%{_datadir}/gap
%{_desktopdir}/%{name}.desktop
