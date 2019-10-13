from pathlib import Path
from typing import List

from sitedeployer.Projekt.Project._Project.Project import Project


class fw_Project(
    Project
):
    def NAME(self) -> str:
        return 'fw'
    
    def pythonanywhere_username(self) -> str:
        return 'getfw'

    def github_url_type(self) -> str:
        return 'ssh'

    def version_list(self) -> List[int]:
        return [2019, 2, 0]

    def is_uninstall_as_package_supported(self) -> bool:
        return True

    def package_executables(self) -> List[str]:
        return [
            'fw',
            'fw.sh',
            'fw.bat',
            'fw_.py',
            'fw.py'
        ]


    def PATHDIRS_packages_to_upload_to_testpypi(self) -> List[Path]:
        return [
            # Path('src/fw'),
            # Path('src/fw_aces'),
            # Path('src/fw_alembic'),
            # Path('src/fw_arnold'),
            # Path('src/fw_behave'),
            # Path('src/fw_blender'),
            # Path('src/fw_blosc'),
            # Path('src/fw_bzip2'),
            # Path('src/fw_catch2'),
            # Path('src/fw_cmake'),
            # Path('src/fw_d3elight'),
            # Path('src/fw_d3equalizer'),
            # Path('src/fw_docutils'),
            # Path('src/fw_doxygen'),
            # Path('src/fw_easyprofiler'),
            # Path('src/fw_embree'),
            # Path('src/fw_ffmpeg'),
            # Path('src/fw_freeglut'),
            # Path('src/fw_freetype'),
            # Path('src/fw_giflib'),
            # Path('src/fw_glew'),
            # Path('src/fw_glfw3'),
            # Path('src/fw_glu'),
            # Path('src/fw_houdini'),
            # Path('src/fw_hugo'),
            # Path('src/fw_ilmbase'),
            # Path('src/fw_ilmbaseopenexr'),
            # Path('src/fw_katana'),
            # Path('src/fw_libflatarray'),
            # Path('src/fw_libpng'),
            # Path('src/fw_librix'),
            # Path('src/fw_libtiff'),
            # Path('src/fw_libwebp'),
            # Path('src/fw_libyaml'),
            # Path('src/fw_llvm'),
            # Path('src/fw_mari'),
            # Path('src/fw_materialx'),
            # Path('src/fw_maxwell'),
            # Path('src/fw_maya'),
            # Path('src/fw_mayadevkit'),
            # Path('src/fw_mc'),
            # Path('src/fw_miarmy'),
            # Path('src/fw_mozjpeg'),
            # Path('src/fw_natron'),
            # Path('src/fw_ninja'),
            # Path('src/fw_nuke'),
            # Path('src/fw_ocio'),
            # Path('src/fw_oiio'),
            # Path('src/fw_opendcx'),
            # Path('src/fw_openexr'),
            # Path('src/fw_openexrviewers'),
            # Path('src/fw_opensubdiv'),
            # Path('src/fw_openvdb'),
            # Path('src/fw_osl'),
            # Path('src/fw_otio'),
            # Path('src/fw_partio'),
            # Path('src/fw_patch'),
            # Path('src/fw_pftrack'),
            # Path('src/fw_photoshop'),
            # Path('src/fw_ptex'),
            # Path('src/fw_pthreadswin32'),
            # Path('src/fw_pugixml'),
            # Path('src/fw_pyqt5'),
            # Path('src/fw_pystring'),
            # Path('src/fw_python2'),
            # Path('src/fw_python3'),
            # Path('src/fw_pyyaml'),
            # Path('src/fw_qt'),
            # Path('src/fw_rapidjson'),
            # Path('src/fw_realflow'),
            # Path('src/fw_renderman'),
            # Path('src/fw_rendermanclassic'),
            # Path('src/fw_rendermanexamples'),
            # Path('src/fw_reportlab'),
            # Path('src/fw_rfh'),
            # Path('src/fw_rfm'),
            # Path('src/fw_seexpr'),
            # Path('src/fw_setuptools'),
            # Path('src/fw_spdlog'),
            # Path('src/fw_sphinx'),
            # Path('src/fw_tbb'),
            # Path('src/fw_tinyxml'),
            # Path('src/fw_tinyxml2'),
            # Path('src/fw_tractor'),
            # Path('src/fw_usd'),
            # Path('src/fw_vagrant'),
            # Path('src/fw_valgrind'),
            # Path('src/fw_virtualenv'),
            # Path('src/fw_wheel'),
            # Path('src/fw_yamlcpp'),
            # Path('src/fw_zlib'),
            # Path('src/fw_zstd'),
            # Path('src/fw_ln'),
            # Path('src/fw_sola')
        ]