[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/nfa-vfxim/tk-houdini-arnold?include_prereleases)](https://github.com/nfa-vfxim/tk-houdini-arnold) 
[![GitHub issues](https://img.shields.io/github/issues/nfa-vfxim/tk-houdini-arnold)](https://github.com/nfa-vfxim/tk-houdini-arnold/issues) 


# Arnold Render Node

[![Documentation](https://img.shields.io/badge/documentation-blue?style=for-the-badge)](https://wiki.vfxim.nl)

A Shotgun Toolkit app to render in Houdini with the Arnold render engine and Deadline.

> Supported engines: tk-houdini

## Requirements

| ShotGrid version | Core version | Engine version |
|------------------|--------------|----------------|
| -                | -            | -              |

## Configuration

### Templates

| Name                     | Description                                                                          | Default value | Fields                                                          |
|--------------------------|--------------------------------------------------------------------------------------|---------------|-----------------------------------------------------------------|
| `work_file_template`     | A template which describes the current Houdini work hip file. Used to fetch version. |               | context, version, [name], *                                     |
| `output_render_template` | A template which describes the output of the beauty render.                          |               | context, version, SEQ, [aov_name], [name], [width], [height], * |
| `output_aov_template`    | A template which describes the output of the AOV renders.                            |               | context, version, SEQ, [aov_name], [name], [width], [height], * |
| `output_ass_template`    | A template which describes the output of the ASS files.                              |               | context, version, SEQ, [name], [width], [height], *             |


