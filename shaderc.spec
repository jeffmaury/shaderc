# Release 2019.0
%global commit          34c412f21f945f4ef6ed4453f8b5dc4bb9d739e4
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global snapshotdate    20190609
%global gitversion      v2019.0

# Need to keep this in sync with spirv-tools
%global spirv_commit    2297d4a3dfcbfd2a8b4312fab055ae26e3289fd3
%global spirv_version   v2019.1

Name:           shaderc
Version:        2019.0
Release:        2%{?dist}
Summary:        A collection of tools, libraries, and tests for Vulkan shader compilation

License:        ASL 2.0
URL:            https://github.com/google/shaderc
Source0:        %url/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

# https://github.com/google/shaderc/pull/463
Patch0:         https://patch-diff.githubusercontent.com/raw/google/shaderc/pull/463.patch#/0001-Fix-the-link-order-of-libglslang-and-libHLSL.patch
# Patch to unbundle 3rd party code
Patch1:         0001-Drop-third-party-code-in-CMakeLists.txt.patch

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  python3-devel
BuildRequires:  glslang-devel
BuildRequires:  spirv-headers-devel
BuildRequires:  spirv-tools
BuildRequires:  spirv-tools-devel

%description
A collection of tools, libraries and tests for shader compilation.

Shaderc aims to to provide:
 - a command line compiler with GCC- and Clang-like usage, for better
   integration with build systems
 - an API where functionality can be added without breaking existing clients
 - an API supporting standard concurrency patterns across multiple
   operating systems
 - increased functionality such as file #include support


%package    -n  glslc
Summary:        A command line compiler for GLSL/HLSL to SPIR-V

%description -n glslc
A command line compiler for GLSL/HLSL to SPIR-V.


%package    -n  libshaderc
Summary:        A library for compiling shader strings into SPIR-V

%description -n libshaderc
A library for compiling shader strings into SPIR-V.


%package -n     libshaderc-devel
Summary:        Development files for libshaderc
Requires:       libshaderc%{?_isa} = %{version}-%{release}

%description -n libshaderc-devel
A library for compiling shader strings into SPIR-V.

Development files for libshaderc.


%package -n     libshaderc-static
Summary:        A library for compiling shader strings into SPIR-V (static libraries)

%description -n libshaderc-static
A library for compiling shader strings into SPIR-V.

Static libraries for libshaderc.


%prep
%autosetup -p1 -n %{name}-%{commit}

rm -rf third_party

# Stolen from Gentoo
# Create build-version.inc since we want to use our packaged
# SPIRV-Tools and glslang
echo \"shaderc $(grep -m1 -o '^v[[:digit:]]\{4\}\.[[:digit:]]\(-dev\)\?' CHANGES) %{gitversion}\" \
        > glslc/src/build-version.inc
echo \"spirv-tools $(grep -m1 -o '^v[[:digit:]]\{4\}\.[[:digit:]]\(-dev\)\?' /usr/share/doc/spirv-tools/CHANGES) %{spirv_version}\" \
        >> glslc/src/build-version.inc
echo \"glslang \'\'\" >> glslc/src/build-version.inc


%build
mkdir %_target_platform
cd %_target_platform
# We disable the tests because they don't work with our unbundling of 3rd party.
# See https://github.com/google/shaderc/issues/470
%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DCMAKE_SKIP_RPATH=True \
        -DSHADERC_SKIP_TESTS=True \
        -DPYTHON_EXE=%{__python3} \
        -GNinja ..
%ninja_build


%install
%ninja_install -C %_target_platform


%check
ctest -V


%files -n glslc
%doc glslc/README.asciidoc
%license LICENSE
%{_bindir}/glslc


%files -n libshaderc
%doc AUTHORS CHANGES CONTRIBUTORS README.md
%license LICENSE
%{_libdir}/libshaderc_shared.so.1*


%files -n libshaderc-devel
%{_includedir}/%{name}/
%{_libdir}/libshaderc_shared.so
%{_libdir}/pkgconfig/shaderc.pc


%files -n libshaderc-static
%license LICENSE
%{_libdir}/libshaderc.a
%{_libdir}/libshaderc_combined.a
%{_libdir}/pkgconfig/shaderc_static.pc
%{_libdir}/pkgconfig/shaderc_combined.pc



%changelog
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 00:18:18 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 2019.0-1
- Release 2019.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2018.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 03 2018 Robert-André Mauchin <zebob.m@gmail.com> - 2018.0-1
- Release 2018.0

* Mon Sep 24 2018 Robert-André Mauchin <zebob.m@gmail.com> - 2017.2-1
- Initial build

