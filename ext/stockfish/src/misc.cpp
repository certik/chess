/*
  Stockfish, a UCI chess playing engine derived from Glaurung 2.1
  Copyright (C) 2004-2008 Tord Romstad (Glaurung author)
  Copyright (C) 2008-2010 Marco Costalba, Joona Kiiski, Tord Romstad

  Stockfish is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  Stockfish is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


////
//// Includes
////

#if !defined(_MSC_VER)

#  include <sys/time.h>
#  include <sys/types.h>
#  include <unistd.h>
#  if defined(__hpux)
#     include <sys/pstat.h>
#  endif

#else

#define _CRT_SECURE_NO_DEPRECATE
#include <windows.h>
#include <sys/timeb.h>

#endif

#if !defined(NO_PREFETCH)
#  include <xmmintrin.h>
#endif

#include <cassert>
#include <cstdio>
#include <iomanip>
#include <iostream>
#include <sstream>

#include "bitcount.h"
#include "misc.h"
#include "thread.h"

using namespace std;

/// Version number. If this is left empty, the current date (in the format
/// YYMMDD) is used as a version number.

static const string EngineVersion = "1.8";
static const string AppName = "Stockfish";
static const string AppTag  = "";


////
//// Variables
////

bool Chess960;

uint64_t dbg_cnt0 = 0;
uint64_t dbg_cnt1 = 0;

bool dbg_show_mean = false;
bool dbg_show_hit_rate = false;


////
//// Functions
////

void dbg_hit_on(bool b) {

    assert(!dbg_show_mean);
    dbg_show_hit_rate = true;
    dbg_cnt0++;
    if (b)
        dbg_cnt1++;
}

void dbg_hit_on_c(bool c, bool b) {

    if (c)
        dbg_hit_on(b);
}

void dbg_before() {

    assert(!dbg_show_mean);
    dbg_show_hit_rate = true;
    dbg_cnt0++;
}

void dbg_after() {

    assert(!dbg_show_mean);
    dbg_show_hit_rate = true;
    dbg_cnt1++;
}

void dbg_mean_of(int v) {

    assert(!dbg_show_hit_rate);
    dbg_show_mean = true;
    dbg_cnt0++;
    dbg_cnt1 += v;
}

void dbg_print_hit_rate() {

  cout << "Total " << dbg_cnt0 << " Hit " << dbg_cnt1
       << " hit rate (%) " << (dbg_cnt1*100)/(dbg_cnt0 ? dbg_cnt0 : 1) << endl;
}

void dbg_print_mean() {

  cout << "Total " << dbg_cnt0 << " Mean "
       << (float)dbg_cnt1 / (dbg_cnt0 ? dbg_cnt0 : 1) << endl;
}

void dbg_print_hit_rate(ofstream& logFile) {

  logFile << "Total " << dbg_cnt0 << " Hit " << dbg_cnt1
          << " hit rate (%) " << (dbg_cnt1*100)/(dbg_cnt0 ? dbg_cnt0 : 1) << endl;
}

void dbg_print_mean(ofstream& logFile) {

  logFile << "Total " << dbg_cnt0 << " Mean "
          << (float)dbg_cnt1 / (dbg_cnt0 ? dbg_cnt0 : 1) << endl;
}

/// engine_name() returns the full name of the current Stockfish version.
/// This will be either "Stockfish YYMMDD" (where YYMMDD is the date when the
/// program was compiled) or "Stockfish <version number>", depending on whether
/// the constant EngineVersion (defined in misc.h) is empty.

const string engine_name() {

  const string cpu64(CpuHas64BitPath ? " 64bit" : "");

  if (!EngineVersion.empty())
      return AppName + " " + EngineVersion + cpu64;

  string date(__DATE__); // From compiler, format is "Sep 21 2008"
  string months("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec");

  size_t mon = 1 + months.find(date.substr(0, 3)) / 4;

  stringstream s;
  string day = (date[4] == ' ' ? date.substr(5, 1) : date.substr(4, 2));

  string name = AppName + " " + AppTag + " ";

  s << name << date.substr(date.length() - 2) << setfill('0')
    << setw(2) << mon << setw(2) << day << cpu64;

  return s.str();
}


/// get_system_time() returns the current system time, measured in
/// milliseconds.

int get_system_time() {

#if defined(_MSC_VER)
    struct _timeb t;
    _ftime(&t);
    return int(t.time*1000 + t.millitm);
#else
    struct timeval t;
    gettimeofday(&t, NULL);
    return t.tv_sec*1000 + t.tv_usec/1000;
#endif
}


/// cpu_count() tries to detect the number of CPU cores.

#if !defined(_MSC_VER)

#  if defined(_SC_NPROCESSORS_ONLN)
int cpu_count() {
  return Min(sysconf(_SC_NPROCESSORS_ONLN), MAX_THREADS);
}
#  elif defined(__hpux)
int cpu_count() {
  struct pst_dynamic psd;
  if (pstat_getdynamic(&psd, sizeof(psd), (size_t)1, 0) == -1)
      return 1;

  return Min(psd.psd_proc_cnt, MAX_THREADS);
}
#  else
int cpu_count() {
  return 1;
}
#  endif

#else

int cpu_count() {
  SYSTEM_INFO s;
  GetSystemInfo(&s);
  return Min(s.dwNumberOfProcessors, MAX_THREADS);
}

#endif


/*
  From Beowulf, from Olithink
*/
#ifndef _WIN32
/* Non-windows version */
int Bioskey()
{
  fd_set          readfds;
  struct timeval  timeout;

  FD_ZERO(&readfds);
  FD_SET(fileno(stdin), &readfds);
  /* Set to timeout immediately */
  timeout.tv_sec = 0;
  timeout.tv_usec = 0;
  select(16, &readfds, 0, 0, &timeout);

  return (FD_ISSET(fileno(stdin), &readfds));
}

#else
/* Windows-version */
#include <windows.h>
#include <conio.h>
int Bioskey()
{
    static int      init = 0,
                    pipe;
    static HANDLE   inh;
    DWORD           dw;
    /* If we're running under XBoard then we can't use _kbhit() as the input
     * commands are sent to us directly over the internal pipe */

#if defined(FILE_CNT)
    if (stdin->_cnt > 0)
        return stdin->_cnt;
#endif
    if (!init) {
        init = 1;
        inh = GetStdHandle(STD_INPUT_HANDLE);
        pipe = !GetConsoleMode(inh, &dw);
        if (!pipe) {
            SetConsoleMode(inh, dw & ~(ENABLE_MOUSE_INPUT | ENABLE_WINDOW_INPUT));
            FlushConsoleInputBuffer(inh);
        }
    }
    if (pipe) {
        if (!PeekNamedPipe(inh, NULL, 0, NULL, &dw, NULL))
            return 1;
        return dw;
    } else {
        // Count the number of unread input records, including keyboard,
        // mouse, and window-resizing input records.
        GetNumberOfConsoleInputEvents(inh, &dw);
        if (dw <= 0)
            return 0;

        // Read data from console without removing it from the buffer
        INPUT_RECORD rec[256];
        DWORD recCnt;
        if (!PeekConsoleInput(inh, rec, Min(dw, 256), &recCnt))
            return 0;

        // Search for at least one keyboard event
        for (DWORD i = 0; i < recCnt; i++)
            if (rec[i].EventType == KEY_EVENT)
                return 1;

        return 0;
    }
}

#endif

/// prefetch() preloads the given address in L1/L2 cache. This is a non
/// blocking function and do not stalls the CPU waiting for data to be
/// loaded from RAM, that can be very slow.
#if defined(NO_PREFETCH)
void prefetch(char*) {}
#else

void prefetch(char* addr) {

#if defined(__INTEL_COMPILER) || defined(__ICL)
   // This hack prevents prefetches to be optimized away by
   // Intel compiler. Both MSVC and gcc seems not affected.
   __asm__ ("");
#endif

  _mm_prefetch(addr, _MM_HINT_T2);
  _mm_prefetch(addr+64, _MM_HINT_T2); // 64 bytes ahead
}

#endif

