Summary:	Groups, Algorithms and Programming
Name:		gap
Version:	4.2
Release:	1
Copyright:	distributable
Group:		Applications/Math
Group(de):	Applikationen/Mathematik
Group(pl):	Aplikacje/Matematyczne
URL:		http://www-gap.dcs.st-and.ac.uk/gap
Source0:	ftp://ftp-gap.dcs.st-and.ac.uk/pub/gap/gap4/%{name}4r2.zoo
Patch0:		%{name}-gac.patch
BuildRequires:	unzoo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GAP is a free, open and extensible software package for computation in
discrete abstract algebra.

%prep
%setup -q -c -T
unzoo -x %{SOURCE0}
%patch0 -p1

%build
cd gap4r2
mv cnf/configure.in cnf/configure.bak
sed -e 's/GP_CFLAGS//g' cnf/configure.bak > cnf/configure.in
%{__make} -C cnf configure.out
%configure2_13

mkdir -p bin/%{_target_platform}
cp cnf/configure.out bin/%{_target_platform}/configure
cd bin/%{_target_platform}
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/gap/pkg,%{_examplesdir}/gap}

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
mv new/manual.ps supplement.ps
mv ext/manual.ps prgmanual.ps
mv prg/manual.ps prgtutorial.ps
mv ref/manual.ps refman.ps
mv tut/manual.ps tutorial.ps

gzip -9nf *.ps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc gap4r2/doc/*.ps.gz gap4r2/doc/htm/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/gap
%{_examplesdir}/gap
