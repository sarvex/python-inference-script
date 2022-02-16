﻿// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT license.

#pragma once

#ifdef USE_FMTLIB
#include <fmt/printf.h>
#else
#include <cstdarg>
#include <cstdlib>
#endif

#include <algorithm>
#include <codecvt>
#include <cstdint>
#include <locale>
#include <sstream>
#include <string>
#include <vector>

namespace pyis {

std::vector<std::string> split_str(const std::string& s, const char* delim = " \r\n\t", bool remove_empty = true);

std::string join_str(const std::vector<std::string>& tokens, const std::string& delim);

std::string& ltrim_str(std::string& str, const std::string& chars = "\t\n\v\f\r ");

std::string& rtrim_str(std::string& str, const std::string& chars = "\t\n\v\f\r ");

std::string& trim_str(std::string& str, const std::string& chars = "\t\n\v\f\r ");

bool str_ends_with(std::string const& str, std::string const& suffix);

std::string to_lower(const std::string& s);

#ifdef USE_FMTLIB
template <typename... Args>
std::string fmt_str(const char* fmt, Args&&... args) {
    return fmt::sprintf(fmt, std::forward<Args>(args)...);
}
#else
std::string fmt_str(const char* format, ...);
#endif

std::wstring str_to_wstr(const std::string& str);

std::string wstr_to_str(const std::wstring& wstr);

bool is_CJK(char32_t c);

bool is_accent(char32_t c);

char32_t strip_accent(char32_t c);

void replace_all(std::string& data, const std::string& str_to_search, const std::string& str_to_replace);

bool is_unicode_category_L(const char32_t& ch);

bool is_unicode_category_N(const char32_t& ch);

bool is_unicode_category_Z(const char32_t& ch);

bool not_category_LNZ(const char32_t& ch);

class Ustring : public std::u32string {
  public:
    Ustring();
    explicit Ustring(char* str);
    explicit Ustring(const char* str);
    explicit Ustring(std::string& str);
    explicit Ustring(const std::string& str);
    explicit Ustring(char32_t* str);
    explicit Ustring(const char32_t* str);
    explicit Ustring(std::u32string& str);
    explicit Ustring(std::u32string&& str);
    explicit Ustring(const std::u32string& str);
    explicit Ustring(const std::u32string&& str);

    explicit operator std::string();
    explicit operator std::string() const;

  private:
    using utf8_converter = std::wstring_convert<std::codecvt_utf8<char32_t>, char32_t>;
};

}  // namespace pyis

namespace std {
template <>
struct hash<pyis::Ustring> {
    size_t operator()(const pyis::Ustring& str) const noexcept {
        hash<u32string> standard_hash;
        return standard_hash(static_cast<u32string>(str));
    }
};
}  // namespace std
