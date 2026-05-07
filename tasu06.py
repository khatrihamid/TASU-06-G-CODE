import inkex
import os


ROW_TOLERANCE = 0.001
POSITION_TOLERANCE = 0.0005


class Tasu(inkex.EffectExtension):

    def add_arguments(self, pars):

        pars.add_argument("--directory")

        pars.add_argument("--filename")

        pars.add_argument("--tool_power_command")

        pars.add_argument("--tool_off_command")

        pars.add_argument("--dwell_time", type=float)

        pars.add_argument("--start_position", default="left_bottom")

        pars.add_argument("--zig_zag_sort", type=inkex.Boolean, default=False)

    def get_punches(self):

        punches = []

        for element in self.svg.selection.values():

            try:

                bbox = element.bounding_box()

                x = (bbox.left + bbox.right) / 2

                y = (bbox.top + bbox.bottom) / 2

                punches.append((x, y))

            except Exception as e:

                inkex.errormsg(str(e))

        return punches

    def get_start_point(self, punches):

        min_x = min(point[0] for point in punches)

        if self.options.start_position == "left_top":

            y = min(point[1] for point in punches)

        else:

            y = max(point[1] for point in punches)

        return min_x, y

    def sort_zig_zag(self, punches):

        rows = {}

        for x, y in punches:

            row_key = round(y / ROW_TOLERANCE) * ROW_TOLERANCE

            rows.setdefault(row_key, []).append((x, y))

        reverse_rows = self.options.start_position == "left_bottom"

        sorted_rows = sorted(rows.items(), key=lambda row: row[0], reverse=reverse_rows)

        sorted_punches = []

        left_to_right = True

        for unused_row_key, row_points in sorted_rows:

            sorted_punches.extend(
                sorted(row_points, key=lambda point: point[0], reverse=not left_to_right)
            )

            left_to_right = not left_to_right

        return sorted_punches

    def add_move(self, gcode, current_position, x, y, compact=False):

        if current_position:

            current_x, current_y = current_position

            same_x = abs(current_x - x) <= POSITION_TOLERANCE

            same_y = abs(current_y - y) <= POSITION_TOLERANCE

            if same_x and same_y:

                return current_position

            if compact:

                command = ["G0"]

                if not same_x:

                    command.append(f"X{x:.3f}")

                if not same_y:

                    command.append(f"Y{y:.3f}")

                gcode.append(" ".join(command))

                return x, y

        gcode.append(
            f"G0 X{x:.3f} Y{y:.3f}"
        )

        return x, y

    def effect(self):

        output_path = os.path.join(
            self.options.directory,
            self.options.filename
        )

        gcode = []

        gcode.append("G21")
        gcode.append("G90")

        punches = self.get_punches()

        current_position = None

        if punches:

            start_x, start_y = self.get_start_point(punches)

            current_position = self.add_move(
                gcode,
                current_position,
                start_x,
                start_y
            )

        if self.options.zig_zag_sort:

            punches = self.sort_zig_zag(punches)

        for x, y in punches:

            current_position = self.add_move(
                gcode,
                current_position,
                x,
                y,
                self.options.zig_zag_sort
            )

            gcode.append(
                self.options.tool_power_command
            )

            gcode.append(
                f"G4 P{self.options.dwell_time}"
            )

            gcode.append(
                self.options.tool_off_command
            )

        gcode.append("M2")

        with open(output_path, "w") as f:

            f.write("\n".join(gcode))

        inkex.errormsg(
            f"{len(punches)} punches generated\n\n{output_path}"
        )


if __name__ == '__main__':

    Tasu().run()
