Summary:	Groups, Algorithms and Programming
Summary(pl):	Grupy, Algorytmy i Programowanie
Name:		gap
Version:	4.2
Release:	3
License:	distributable
Group:		Applications/Math
Source0:	ftp://ftp-gap.dcs.st-and.ac.uk/pub/gap/gap4/%{name}4r2.zoo
Source1:	%{name}.desktop
Patch0:		%{name}-gac.patch
URL:		http://www-gap.dcs.st-and.ac.uk/gap/
BuildRequires:	unzoo
BuildRequires:	tetex-dvips
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GAP is a free, open and extensible software package for computation in
discrete abstract algebra.

%description -l pl
GAP jest darmowym, otwartym i rozszerzalnym pakietem oprogramowania do
obliczeñ dyskretnej abstrakcyjnej algebry.

%package share_package_demo
Summary:	Example share package for GAP
Summary(pl):	¬ród³a przyk³adowego pakietu wspó³dzielonego dla GAP
Group:		Applications/Math
Requires:	gap >= 4.0

%description share_package_demo
This is an example how to add a share package to GAP (version 4).

%description share_package_demo -l pl
Przyk³ad, jak dodaæ wspó³dzielony pakiet do GAP (wersja 4).

%prep
%setup -q -c -T
unzoo -x %{SOURCE0}
%patch0 -p1

%build
cd gap4r2
mv -f cnf/configure.in cnf/configure.bak
sed -e 's/GP_CFLAGS//g' cnf/configure.bak > cnf/configure.in
%{__make} -C cnf configure.out
%configure2_13

mkdir -p bin/%{_target_platform}
cp -f cnf/configure.out bin/%{_target_platform}/configure
cd bin/%{_target_platform}
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/gap/pkg,%{_examplesdir}/gap,%{_applnkdir}/Scientific/Mathematics}

cd gap4r2

cp -a sysinfo.gap grp lib prim small src tbl tom trans tst $RPM_BUILD_ROOT%{_datadir}/gap/
cp -a pkg/example/* $RPM_BUILD_ROOT%{_examplesdir}/gap

install bin/%{_target_platform}/gap $RPM_BUILD_ROOT%{_bindir}/%{_target_platform}-gap
install bin/%{_target_platform}/gac $RPM_BUILD_ROOT%{_bindir}

cat <<EOF > $RPM_BUILD_ROOT%{_bindir}/gap
#!/bin/sh
[ -z "\$GAP_MEM" ] && GAP_MEM=12m
exec %{_bindir}/%{_target_platform}-gap -m \$GAP_MEM -l %{_datadir}/gap \$*
EOF

cd doc
for i in ext new prg ref tut ; do
	(cd $i ; dvips manual.dvi -o )
done
dvips fullindex.dvi -o
mv -f new/manual.ps supplement.ps
mv -f ext/manual.ps prgmanual.ps
mv -f prg/manual.ps prgtutorial.ps
mv -f ref/manual.ps refman.ps
mv -f tut/manual.ps tutorial.ps

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Scientific/Mathematics/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc gap4r2/doc/*.ps gap4r2/doc/htm/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/gap
%{_applnkdir}/Scientific/Mathematics/*

%files share_package_demo
%defattr(644,root,root,755)
%{_examplesdir}/gap
