package body Number is

    package body Class_Number is

--        function New_Number (arg1 : Integer; arg2 : Integer) return Number
--        is
--            N : constant Number := (x => arg1, y => arg2);
--        begin
--            return N;
--        end New_Number;

        function add (this : access Number) return Integer
        is
        begin
            return this.x + this.y;
        end add;

    end Class_Number;

end Number;
