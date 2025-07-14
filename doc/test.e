#using util/math.e;

module program{

    let num: int = 213;

    let numPtr: int* = &num;

    function add(op1, op2: int;) {
        return op1 + op2;
    }

    class string {
        private let textPtr: char*;
        public function string(text: char*;) {
            this->textPtr = new offset(text);
        }
    }

    function div(op1, op2: int;) {
        index = 0;
        while (op1 > 0) {
            op1 -= op2;
            index += 1;
        }

        return index;
    }

    function inc_col <T> (op1: list<T>) {
        op1.foreach(elemant => {});
    }

    enum types {
        char, short, int, long, float, double
    }

    let word = string("Hello, World!");

    let type = types::int;

}
