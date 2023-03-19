Summary:	APFS FUSE Driver for Linux
Summary(pl.UTF-8):	Sterownik APFS FUSE dla Linuksa
Name:		apfs-fuse
Version:	0
%define	gitref	66b86bd525e8cb90f9012543be89b1f092b75cf3
%define	snap	20230313
%define	rel	1
Release:	0.%{snap}.%{rel}
License:	GPL v2
Group:		Applications/System
Source0:	https://github.com/sgan81/apfs-fuse/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	d0c3a601dd7e3e8f8f7ef4f4ab244efa
%define	lzfse_gitref	e634ca58b4821d9f3d560cdc6df5dec02ffc93fd
Source1:	https://github.com/lzfse/lzfse/archive/%{lzfse_gitref}/lzfse-%{lzfse_gitref}.tar.gz
# Source1-md5:	e5533c906e31ec2ac6a3c412342d885f
Patch0:		%{name}-cmake.patch
URL:		https://github.com/sgan81/apfs-fuse
BuildRequires:	bzip2-devel
BuildRequires:	cmake >= 3.0
BuildRequires:	libfuse3-devel >= 3
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project is a read-only FUSE driver for the new Apple File System.
It also supports software encrypted volumes and fusion drives.
Firmlinks are not supported yet.

Be aware that not all compression methods are supported yet (only the
ones encountered by author so far). Thus, the driver may return
compressed files instead of uncompressed ones. Although most of the
time it should just report an error.

%description -l pl.UTF-8
Ten projekt to sterownik do nowego systemu plików APFS (Apple File
System), działający w trybie tylko do odczytu. Obsługuje zaszyfrowane
programowo wolumeny oraz napędy łączone. Firmlinki nie są jeszcze
obsługiwane.

Uwaga: obecnie nie wszystkie metody kompresji są obsługiwane (tylko
te, które napotkał autor) - więc sterownik może zwrócić skompresowane
pliki zamiast zdekompresowanych; choć w większości przypadków powinien
tylko zgłosić błąd.

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1

tar xf %{SOURCE1} -C 3rdparty/lzfse --strip-components=1

%build
install -d build
cd build
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/apfs-fuse
%attr(755,root,root) %{_bindir}/apfsutil
