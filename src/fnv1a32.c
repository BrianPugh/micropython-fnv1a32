#include "py/dynruntime.h"

static uint32_t _hash_loop(uint32_t state, uint8_t *data, uint32_t size){
    for(uint32_t i=0; i < size; i++){
        state ^= data[i];
        state *= 0x01000193;
    }
    return state;
}

static mp_obj_t _fnv1a32(mp_obj_t data_obj, mp_obj_t state_obj, mp_obj_t chunk_size_obj) {
    mp_buffer_info_t buf_info;
    uint32_t state = mp_obj_get_int(state_obj);

    if(mp_get_buffer(data_obj, &buf_info, MP_BUFFER_READ)){
        // Is a buffer-like object
        state = _hash_loop(state, buf_info.buf, buf_info.len);
    }
    else{
        // Is a file-like object
        mp_int_t chunk_size = mp_obj_get_int(chunk_size_obj);
        uint8_t *buffer = m_malloc(chunk_size);
        mp_obj_t buffer_obj = mp_obj_new_bytearray_by_ref(chunk_size, buffer);
        mp_obj_t readinto_method = mp_load_attr(data_obj, MP_QSTR_readinto);
        mp_int_t amount_read;
        do{
            mp_obj_t amount_read_obj = mp_call_function_n_kw(readinto_method, 1, 0, &buffer_obj);
            amount_read = mp_obj_get_int(amount_read_obj);
            state = _hash_loop(state, buffer, amount_read);
        }while(amount_read);
    }

    return mp_obj_new_int(state);
}
static MP_DEFINE_CONST_FUN_OBJ_3(_fnv1a32_obj, _fnv1a32);

mp_obj_t mpy_init(mp_obj_fun_bc_t *self, size_t n_args, size_t n_kw, mp_obj_t *args) {
    MP_DYNRUNTIME_INIT_ENTRY

    mp_store_global(MP_QSTR__fnv1a32, MP_OBJ_FROM_PTR(&_fnv1a32_obj));

    MP_DYNRUNTIME_INIT_EXIT
}
