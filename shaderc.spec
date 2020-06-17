# Release 2020.1
%global commit          7c2aa93903558f017f31b35df163bce5fe849f45
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global snapshotdate    20200617

# Glslang revision from packaged version
%global glslang_version SDK-candidate-2-11-gc9b28b9f

Name:           shaderc
Version:        2020.1
Release:        1%{?dist}
Summary:        A collection of tools, libraries, and tests for Vulkan shader compilation

License:        ASL 2.0
URL:            https://github.com/google/shaderc
Source0:        %url/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

# https://github.com/google/shaderc/pull/463
Patch0:         https://patch-diff.githubusercontent.com/raw/google/shaderc/pull/463.patch#/0001-Fix-the-link-order-of-libglslang-and-libHLSL.patch
# Patch to unbundle 3rd party code
Patch1:         0001-Drop-third-party-code-in-CMakeLists.txt.patch
# Fix bug in latest version (to drop in next version)
Patch2:         0001-Rolling-5-dependencies-and-fixing-build.patch

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
echo \"shaderc $(grep -m1 -o '^v[[:digit:]]\{4\}\.[[:digit:]]\(-dev\)\? [[:digit:]]\{4\}-[[:digit:]]\{2\}-[[:digit:]]\{2\}$' CHANGES)\" \
        > glslc/src/build-version.inc
echo \"spirv-tools $(grep -m1 -o '^v[[:digit:]]\{4\}\.[[:digit:]]\(-dev\)\? [[:digit:]]\{4\}-[[:digit:]]\{2\}-[[:digit:]]\{2\}$' /usr/share/doc/spirv-tools/CHANGES)\" \
        >> glslc/src/build-version.inc
echo \"glslang %{glslang_version}\" >> glslc/src/build-version.inc

# Point to correct include
sed -i 's|SPIRV/GlslangToSpv.h|glslang/SPIRV/GlslangToSpv.h|' libshaderc_util/src/compiler.cc

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
* Wed Jun 17 20:15:27 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2020.1-1
- Update to 2020.1

* Sun Feb 02 20:53:01 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 2019.1-1
- Update to 2019.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

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

