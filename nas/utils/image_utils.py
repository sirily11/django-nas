from exif import Image


def get_image_metadata(path: str) -> dict:
    """
    Get Image metadata, if error, return None
    :param path:
    :return:
    """
    with open(path, 'rb') as file:

        ret_data = {}
        try:
            image_metadata = Image(img_file=file)
            if image_metadata.has_exif:

                for info in ['aperture_value', 'brightness_value', 'datetime',
                             'exposure_bias_value', 'exposure_time', 'f_number',
                             'flash', 'focal_length', 'gps_altitude', 'gps_altitude_ref',
                             'gps_dest_bearing', 'gps_dest_bearing_ref',
                             'gps_horizontal_positioning_error', 'gps_img_direction',
                             'gps_img_direction_ref', 'gps_latitude', 'gps_latitude_ref',
                             'gps_longitude', 'gps_longitude_ref', 'gps_speed', 'gps_speed_ref',
                             'has_exif', 'lens_make', 'lens_model', 'lens_specification',
                             'metering_mode', 'model', 'pixel_x_dimension',
                             'pixel_y_dimension', 'resolution_unit', 'scene_capture_type',
                             'scene_type', 'shutter_speed_value', 'software',
                             'subject_area', 'subsec_time_digitized', 'subsec_time_original', 'white_balance',
                             'x_resolution', 'y_resolution']:
                    try:
                        data = getattr(image_metadata, info)
                        if isinstance(getattr(image_metadata, info), tuple):
                            ret_data[info] = list(data)
                        else:
                            data: str
                            ret_data[info] = data.replace("\u0000", '')
                    except:
                        pass
        except Exception as e:
            print(e)

        return ret_data if len(ret_data) > 0 else None
